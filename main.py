import wikipediaapi


if __name__ == '__main__':
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

    page_py = wiki_wiki.page('Python_(programming_language)')

    print()