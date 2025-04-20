import streamlit as st

from query.ml.randomforest import train_random_forest_model
from query.ml.aux import evaluate_model_performance
from query.query import preprocessing_for_classification
from decimal import Decimal, ROUND_UP
import plotly.express as px


def plot_confusion_matrix(cm):
    figs = px.imshow(cm, text_auto=True, color_continuous_scale="Blues")
    figs.update_layout(
        title="Confusion matrix",
        xaxis=dict(title="Predicted Labels", side="bottom"),
        yaxis=dict(title="Real Labels")
    )

    figs.update_layout(
        xaxis=dict(tickmode='linear', tickformat='d'),
        yaxis=dict(tickmode='linear', tickformat='d'),
        width=2000,
        height=550
    )
    return figs


st.set_page_config(page_title="ML Classification", layout="wide")
st.title(":blue[ML Classification]")

st.markdown(
    """:blue[This page allows you to train a classification model with the goal of predicting the 
        delay of a flight. Once training is complete, you can view some metrics that indicate the 
        goodness of the trained model.]
    """)

df = preprocessing_for_classification()
avvia_training = st.sidebar.button("Train Model")

if avvia_training:
    with st.spinner("Training in progress... This may take 5 minutes."):
        model = train_random_forest_model(df)

    st.success("Training completed successfully!")

    st.markdown("# :blue[Model Metrics]")

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
