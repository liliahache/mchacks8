from google.cloud import language_v1

def sample_classify_text(gcs_content_uri):

    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"gcs_content_uri": gcs_content_uri, "type_": type_, "language": language}
    response = client.classify_text(request = {'document': document})

    try:
        first_category = response.categories[0]
        with_slash = str(first_category.name)
        no_slash = with_slash.replace("/", "")
        return no_slash

    except IndexError:
        return ""

    

if __name__ == '__main__':
    print(sample_classify_text('gs://trismegistus_ballsac/input1.txt'))

