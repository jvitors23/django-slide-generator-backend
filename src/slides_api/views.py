import pysbd
import wikipediaapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SlideFeaturesSerializer


def check_wikipedia_page_exists(subject):
    """Given a subject, verify if it has a page on wikipedia"""
    return True


class SlidesAPIView(APIView):
    """Given a subject, max_slides and language returns the slide images and \
    texts."""
    USELESS_SECTIONS = ['Ver também', 'Referências', 'See also', 'References']

    serializer_class = SlideFeaturesSerializer

    @staticmethod
    def get_sentences(text):
        """Breaks section text in sentences, max of 3 sentences per topic"""
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

    def fetch_data_from_wikipedia(self, slide_subject,
                                  max_slides, language='pt'):

        wiki = wikipediaapi.Wikipedia(language)

        subject_page = wiki.page(slide_subject)
        references = [subject_page.fullurl]

        summary_sentences = self.get_sentences(
            subject_page.summary.replace('\n', ''))

        intro_title = slide_subject
        if language == 'pt':
            intro_title = 'Introdução'
        elif language == 'en':
            intro_title = 'Introduction'

        topics = [{'title': intro_title,
                   'subtitle': '',
                   'sentences': summary_sentences,
                   }]

        for section in subject_page.sections:
            if section.title in self.USELESS_SECTIONS:
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
                    num_section_subtopics += 1
                    if num_section_subtopics >= 3 or len(topics) >= \
                            max_slides - 2:
                        break

            if len(topics) >= max_slides - 2:
                break

        return {
            'topics': topics,
            'references': references,
        }

    def post(self, request):
        """Given a subject return slide images and text"""

        serializer = SlideFeaturesSerializer(data=request.data)

        if serializer.is_valid():
            slide_features = serializer.validated_data

            slide_subject = slide_features['subject']
            max_slides = slide_features['max_slides']
            language = slide_features['language']

            wikipedia_content = self.fetch_data_from_wikipedia(
                slide_subject, max_slides, language)

            print(len(wikipedia_content['topics']))

            # Clean the content

            # Get IBM Watson interpretation

            return Response(wikipedia_content)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
