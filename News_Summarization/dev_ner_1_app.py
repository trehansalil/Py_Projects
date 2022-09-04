import gradio as gr

ner_arman = gr.Interface.load(
  'huggingface/BK-V/xlm-roberta-base-finetuned-arman-fa',
  inputs = gr.inputs.Textbox(
    lines = 5,
    placeholder = 'متن را وارد کنید',
    default = 'ناسا در اقدامی مشترک با اسپیس ایکس به مالکیت ایلان ماسک فضانوردان خود را از ایالت مینه سوتا به سمت ایستگاه فضایی بین المللی فرستاد.',
    label = 'Input Text (Persian)'
  )
)

ner_peyma = gr.Interface.load(
  'huggingface/BK-V/xlm-roberta-base-finetuned-peyma-fa',
  inputs = gr.inputs.Textbox(
    lines = 5,
    placeholder = 'متن را وارد کنید',
    default = 'ناسا در اقدامی مشترک با اسپیس ایکس به مالکیت ایلان ماسک فضانوردان خود را از ایالت مینه سوتا به سمت ایستگاه فضایی بین المللی فرستاد.',
    label = 'Input Text (Persian)'
  )
)

gr.Parallel(ner_arman , ner_peyma).launch(enable_queue=True, share=True)