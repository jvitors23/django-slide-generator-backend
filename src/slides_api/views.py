import wikipediaapi
import wikipedia
import pysbd

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SlideFeaturesSerializer


class SlidesAPIView(APIView):
    """Slides API - Given slide features (subject, topics, sources)
    returns the slide images and texts"""

    serializer_class = SlideFeaturesSerializer

    @staticmethod
    def get_sentences(text):
        seg = pysbd.Segmenter(language="en", clean=False)
        if len(text) > 512 * 6:
            text = text[:512 * 6]
        sentences = seg.segment(text)
        final_sentences = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences):
                if len(sentences[i] + ' ' + sentences[i + 1]) < 512:
                    final_sentences.append(
                        sentences[i] + ' ' + sentences[i + 1])
                    i += 2
                else:
                    final_sentences.append(sentences[i])
                    i += 1
            else:
                final_sentences.append(sentences[i])
                i += 1

            if len(final_sentences) >= 3:
                break

        sentences_data = []
        for sentence in final_sentences:
            sentences_data.append({
                'content': sentence,
                'keywords': [],
                'images': []
            })

        return sentences_data

    def fetch_data_from_wikipedia(self, slide_subject, language='pt'):
        wikipedia.set_lang(language)
        references = [wikipedia.page(slide_subject).url]
        wikipedia_images = wikipedia.page(slide_subject).images

        wiki = wikipediaapi.Wikipedia(language)
        subject_page = wiki.page(slide_subject)
        summary_sentences = self.get_sentences(
            subject_page.summary.replace('\n', ''))

        topics = [{'title': slide_subject,
                   'subtitle': '',
                   'sentences': summary_sentences,
                   }]
        num_topics = 0
        num_subtopics = 0
        for section in subject_page.sections:
            if len(topics) >= int(len(subject_page.sections) * 0.7):
                break
            if len(section.sections) == 0:
                topic_text = section.full_text().replace(
                    section.title, '').replace('\n', '')
                section_sentences = self.get_sentences(topic_text)
                if len(section_sentences) > 0:
                    topics.append(
                        {'title': section.title,
                         'subtitle': '',
                         'sentences': section_sentences,
                         })
                    num_topics += 1
            num_section_subtopics = 0
            for subsection in section.sections:
                subtopic_text = subsection.full_text().replace(
                    subsection.title, '').replace('\n', '')
                subsection_sentences = self.get_sentences(subtopic_text)
                if len(subsection_sentences) > 0:
                    topics.append(
                        {'title': section.title,
                         'subtitle': subsection.title,
                         'sentences': subsection_sentences,
                         })
                    num_subtopics += 1
                    num_section_subtopics += 1
                    if num_section_subtopics >= 3:
                        break

        return {
            'topics': topics,
            'references': references,
            'wikipedia_images': wikipedia_images
        }

    def post(self, request):
        """Given topics return slide images and text"""

        serializer = SlideFeaturesSerializer(data=request.data)

        if serializer.is_valid():
            slide_features = serializer.validated_data

            slide_subject = slide_features['subject']
            num_slides = slide_features['num_slides']
            language = slide_features['language']

            wikipedia_original_content = self.fetch_data_from_wikipedia(
                slide_subject,
                language)

            # print(len(wikipedia_original_content['topics']))

            # Clean the content

            # Get IBM Watson interpretation

            return Response(wikipedia_original_content)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
