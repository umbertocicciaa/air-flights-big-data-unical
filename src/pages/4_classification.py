import streamlit as st

from ..query.ml.randomforest import train_random_forest_model
from ..query.ml.aux import evaluate_model_performance
from ..query.query import preprocessing_for_classification
from decimal import Decimal, ROUND_UP
import plotly.express as px


def plot_confusion_matrix(cm):
    figs = px.imshow(cm, text_auto=True, color_continuous_scale="Blues")
    figs.update_layout(
        title="Matrice di Confusione",
        xaxis=dict(title="Etichette Predette", side="bottom"),
        yaxis=dict(title="Etichette Reali")
    )

    figs.update_layout(
        xaxis=dict(tickmode='linear', tickformat='d'),
        yaxis=dict(tickmode='linear', tickformat='d'),
        width=2000,
        height=550
    )
    return figs


st.set_page_config(page_title="Classificazione ML", layout="wide")
st.title(":blue[Classificazione ML]")

st.markdown(
    """:blue[Questa pagina permette di addestrare un modello di classificazione con l'obiettivo di prevedere il 
    ritardo di un volo.  Terminato l'addestramento è possibile visualizzare alcune metriche che indicano la bontà del 
    modello addestrato.] """)
df = preprocessing_for_classification()
avvia_training = st.sidebar.button("Addestra Modello")

if avvia_training:
    with st.spinner("Addestramento in corso... Questo potrebbe richiedere 5 minuti."):
        model = train_random_forest_model(df)

    st.success("Addestramento completato con successo!")

    st.markdown("# :blue[Metriche del Modello]")

    confusion_matrix_array, accuracy, f1_score, precision, recall = evaluate_model_performance(model)
    fig = plot_confusion_matrix(confusion_matrix_array)
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        acc = Decimal(str(accuracy)).quantize(Decimal('0.001'), rounding=ROUND_UP)
        f1 = Decimal(str(f1_score)).quantize(Decimal('0.001'), rounding=ROUND_UP)
        st.metric("Accuracy", border=True, value=float(acc))
        st.metric("F1 score", border=True, value=float(f1))

    with col2:
        pre = Decimal(str(precision)).quantize(Decimal('0.001'), rounding=ROUND_UP)
        rec = Decimal(str(recall)).quantize(Decimal('0.001'), rounding=ROUND_UP)
        st.metric("Precision", border=True, value=float(pre))
        st.metric("Recall", border=True, value=float(rec))
