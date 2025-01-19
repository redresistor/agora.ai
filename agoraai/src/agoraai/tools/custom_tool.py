from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
# import arxiv

class ArxivSearcherInput(BaseModel):
    """Input schema for ArxivSearcher."""
    query: str = Field("An Arxiv search query.", description="The query that will be used in the Arxiv search API for results.")
    max_results: int = Field(10, description="The maximum number of search results to return.")

class ArxivSearcherTool(BaseTool):
    name: str = "Arxiv Search Tool"
    description: str = (
        "This tool searches arXiv for the given query using the arXiv API, then returns the search results."
    )
    args_schema: Type[BaseModel] = ArxivSearcherInput

    def _run(self, query: str, max_results: int):
    # def search_arxiv(query, max_results=10):
        """
        Searches arXiv for the given query using the arXiv API, then returns the search results. This is a helper function. In most cases, callers will want to use 'find_relevant_papers( query, max_results )' instead.

        Args:
            query (str): The search query.
            max_results (int, optional): The maximum number of search results to return. Defaults to 10.

        Returns:
            jresults (list): A list of dictionaries. Each dictionary contains fields such as 'title', 'authors', 'summary', and 'pdf_url'

        Example:
            >>> results = search_arxiv("attention is all you need")
            >>> print(results)
        """
        import arxiv
        # # Normalize the query, removing operator keywords
        # query = re.sub(r"[^\s\w]", " ", query.lower())
        # query = re.sub(r"\s(and|or|not)\s", " ", " " + query + " ")
        # query = re.sub(r"[^\s\w]", " ", query.lower())
        # query = re.sub(r"\s+", " ", query).strip()

        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)

        jresults = list()
        for result in search.results():
            r = dict()
            r["entry_id"] = result.entry_id
            r["updated"] = str(result.updated)
            r["published"] = str(result.published)
            r["title"] = result.title
            r["authors"] = [str(a) for a in result.authors]
            r["summary"] = result.summary
            r["comment"] = result.comment
            r["journal_ref"] = result.journal_ref
            r["doi"] = result.doi
            r["primary_category"] = result.primary_category
            r["categories"] = result.categories
            r["links"] = [str(link) for link in result.links]
            r["pdf_url"] = result.pdf_url
            jresults.append(r)

        if len(jresults) > max_results:
            jresults = jresults[0:max_results]
        return jresults

    # return "this is an example of a tool output, ignore it and move along."
