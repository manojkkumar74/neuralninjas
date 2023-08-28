import streamlit as st
from PIL import Image
import pandas as pd

st.title("Online Class Attentiveness")
st.header("Enter App Key")

key=st.text_input("App key")

if key == '':
    st.warning("An app key has not been entered")
    st.stop()
else:
    st.write("App key has been upload")

file_data = st.file_uploader("Upload Image",type=['jpg'])

if file_data == None:
    st.warning("File needs to be uploaded")
    st.stop()
else:
    image = Image.open(file_data)
    st.image(image)

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

# This is how you authenticate.
metadata = (("authorization", "Key {}".format(key)),)

request = service_pb2.PostModelOutputsRequest(
    # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
    model_id="online-class-detector",
    inputs=[
        resources_pb2.Input(
            data=resources_pb2.Data(image=resources_pb2.Image(base64=file_data.getvalue()))
        )
    ],
)
response = stub.PostModelOutputs(request, metadata=metadata)

if response.status.code != status_code_pb2.SUCCESS:
    raise Exception(f"Request failed, status code: {response.status.code}")
for concept in response.outputs[0].data.concepts:
    st.write("%12s: %.2f" % (concept.name, concept.value))