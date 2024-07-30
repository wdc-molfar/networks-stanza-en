# models.py

import stanza


# Download stanza model
def download_model(lang):
    stanza.download(lang)
    return

# Download stanza model
def load_model(lang):
    model = stanza.Pipeline(lang, processors='tokenize,pos,lemma')
    return model


if __name__ == '__main__':
    # Download EN stanza model
    download_model("en")
