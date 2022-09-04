import streamlit as st
from transformers import pipeline
import spacy
from spacy import displacy
import plotly.express as px
import numpy as np
st.set_page_config(page_title="Named Entity Recognition")
st.title("Named Entity Recognition")
st.write("_This web application is intended for educational use, please do not upload any sensitive information._")
st.write("Identifying all geopolitical entities, organizations, people, locations, or dates in a body of text.")

@st.cache(allow_output_mutation=True, show_spinner=False)
def Loading_NLP():
    nlp = spacy.load('en_core_web_sm')
    return nlp
@st.cache(allow_output_mutation=True)
def entRecognizer(entDict, typeEnt):
    entList = [ent for ent in entDict if entDict[ent] == typeEnt]
    return entList
def plot_result(top_topics, scores):
    top_topics = np.array(top_topics)
    scores = np.array(scores)
    scores *= 100
    fig = px.bar(x=scores, y=top_topics, orientation='h',
                 labels={'x': 'Probability', 'y': 'Category'},
                 text=scores,
                 range_x=(0,115),
                 title='Top Predictions',
                 color=np.linspace(0,1,len(scores)),
                 color_continuous_scale="Bluered")
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(texttemplate='%{text:0.1f}%', textposition='outside')
    st.plotly_chart(fig)

with st.spinner(text="Please wait for the models to load. This should take approximately 60 seconds."):
    nlp = Loading_NLP()

text = st.text_area('Enter Text Below:', height=300)
submit = st.button('Generate')
if submit:
    entities = []
    entityLabels = []
    doc = nlp(text)
    for ent in doc.ents:
        entities.append(ent.text)
        entityLabels.append(ent.label_)
    entDict = dict(zip(entities, entityLabels))
    entOrg = entRecognizer(entDict, "ORG")
    entPerson = entRecognizer(entDict, "PERSON")
    entDate = entRecognizer(entDict, "DATE")
    entGPE = entRecognizer(entDict, "GPE")
    entLoc = entRecognizer(entDict, "LOC")
    options = {"ents": ["ORG", "GPE", "PERSON", "LOC", "DATE"]}
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""

    st.subheader("List of Named Entities:")
    st.write("Geopolitical Entities (GPE): " + str(entGPE))
    st.write("People (PERSON): " + str(entPerson))
    st.write("Organizations (ORG): " + str(entOrg))
    st.write("Dates (DATE): " + str(entDate))
    st.write("Locations (LOC): " + str(entLoc))
    st.subheader("Original Text with Entities Highlighted")
    html = displacy.render(doc, style="ent", options=options)
    html = html.replace("\n", " ")
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)