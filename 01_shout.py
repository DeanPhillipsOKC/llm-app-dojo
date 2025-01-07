import gradio as gr

def shout(text):
    return text.upper()

iface = gr.Interface(fn=shout, inputs="text", outputs="text", title="Shout App", description="Enter text and convert it to uppercase", allow_flagging="never")

iface.launch()