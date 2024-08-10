import json

class Reference:
    def __init__(self, authors, year, title, source, url=None, editor=None, translator=None, 
                 edition=None, volume=None, issue=None, pages=None, publisher=None, 
                 publication_date=None, place_of_publication=None, doi=None, access_date=None, 
                 isbn_issn=None, conference_name=None, database=None, medium=None, institution=None, 
                 series_title=None, contributors=None, chapter_title=None, original_publication_date=None, 
                 review=None, lecture_title=None, thesis_type=None, patent_number=None):
        self.authors = authors
        self.year = year
        self.title = title
        self.source = source
        self.url = url
        self.editor = editor
        self.translator = translator
        self.edition = edition
        self.volume = volume
        self.issue = issue
        self.pages = pages
        self.publisher = publisher
        self.publication_date = publication_date
        self.place_of_publication = place_of_publication
        self.doi = doi
        self.access_date = access_date
        self.isbn_issn = isbn_issn
        self.conference_name = conference_name
        self.database = database
        self.medium = medium
        self.institution = institution
        self.series_title = series_title
        self.contributors = contributors
        self.chapter_title = chapter_title
        self.original_publication_date = original_publication_date
        self.review = review
        self.lecture_title = lecture_title
        self.thesis_type = thesis_type
        self.patent_number = patent_number

    def format_apa(self):
        ref = f"{self.authors} ({self.year}). {self.title}. "
        if self.edition:
            ref += f"({self.edition} ed.) "
        ref += f"{self.source}"
        if self.doi:
            ref += f". https://doi.org/{self.doi}"
        elif self.url:
            ref += f". {self.url}"
        return ref

    def format_mla(self):
        ref = f"{self.authors}. \"{self.title}.\" {self.source}, "
        if self.volume:
            ref += f"vol. {self.volume}, "
        if self.issue:
            ref += f"no. {self.issue}, "
        ref += f"{self.year}"
        if self.pages:
            ref += f", pp. {self.pages}"
        if self.doi:
            ref += f", doi:{self.doi}"
        elif self.url:
            ref += f", {self.url}"
        ref += "."
        if self.access_date:
            ref += f" Accessed {self.access_date}."
        return ref

    def format_chicago(self):
        ref = f"{self.authors}. {self.title}. "
        if self.edition:
            ref += f"{self.edition} ed. "
        ref += f"{self.place_of_publication}: {self.publisher}, {self.year}."
        return ref

    def format_vancouver(self):
        ref = f"{self.authors}. {self.title}. {self.source}. {self.year}"
        if self.volume:
            ref += f";{self.volume}"
        if self.issue:
            ref += f"({self.issue})"
        if self.pages:
            ref += f":{self.pages}"
        ref += "."
        return ref

    def format_harvard(self):
        ref = f"{self.authors}, {self.year}. {self.title}. "
        if self.edition:
            ref += f"{self.edition} ed. "
        ref += f"{self.place_of_publication}: {self.publisher}."
        return ref

    def format_ieee(self):
        ref = f"{self.authors}, \"{self.title},\" {self.source}, "
        if self.volume:
            ref += f"vol. {self.volume}, "
        if self.issue:
            ref += f"no. {self.issue}, "
        ref += f"pp. {self.pages}, {self.year}."
        return ref

    def format_ama(self):
        ref = f"{self.authors}. {self.title}. {self.source}. "
        if self.publication_date:
            ref += f"Published {self.publication_date}. "
        ref += f"Accessed {self.access_date}."
        return ref

    def format_acs(self):
        ref = f"{self.authors} {self.title}. {self.source} {self.year}, "
        if self.volume:
            ref += f"{self.volume}"
        if self.issue:
            ref += f"({self.issue})"
        if self.pages:
            ref += f", {self.pages}"
        ref += "."
        return ref

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class ReferenceManager:
    def __init__(self):
        self.references = []

    def add_reference(self, reference):
        self.references.append(reference)

    def remove_reference(self, index):
        if 0 <= index < len(self.references):
            del self.references[index]

    def get_reference(self, index):
        if 0 <= index < len(self.references):
            return self.references[index]
        return None

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([ref.to_dict() for ref in self.references], f)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.references = [Reference.from_dict(ref_data) for ref_data in data]