from django.conf import settings
from ..papers.models import Paper, PaperIsNotRenderableError
from .query import category_search_query


def scrape_papers():
    """
    Download papers from Arxiv's API and insert new ones into the database.
    """
    papers = category_search_query(settings.PAPERS_MACHINE_LEARNING_CATEGORIES)
    for paper in create_papers(papers):
        print("Downloading and rendering {}... ".format(paper.arxiv_id), end="", flush=True)
        try:
            paper.render()
        except PaperIsNotRenderableError:
            print("not renderable")
        else:
            print("success")


def create_papers(papers):
    """
    Create papers that don't already exist. Returns an iterator of papers
    that have been created.
    """
    for paper in papers:
        obj, created = Paper.objects.update_or_create_from_api(paper)
        if created:
            yield obj
