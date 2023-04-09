import os, pickle
from langchain import OpenAI, LLMChain, VectorDBQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores import VectorStore
from langchain.chains import RetrievalQAWithSourcesChain, VectorDBQAWithSourcesChain, load_chain
from langchain.memory import ConversationBufferWindowMemory, ChatMessageHistory



api_key = os.environ.get('OPENAI_API_KEY')

# TODO: langchain has a prebuild QAchain -> VectorDBQA.from_chain_type(llm...)
def load_embed_pickle():
    template = """Assistant is a LLM trained by OpenAI.
    Assistant is a language model designed to assist with academic questions and provide guidance as an academic mentor/tutor. With a vast knowledge base and the ability to process natural language, Assistant can answer questions on a wide range of subjects, including but not limited to, law, economics, history, science, mathematics, and literature.

    As an academic mentor/tutor, Assistant can provide guidance on study habits, essay writing, research methodologies, and exam preparation. Whether you are a high school student, college student, or graduate student, Assistant is equipped to provide the support and guidance you need to succeed academically.

    With its advanced capabilities, Assistant can also help you generate ideas for research projects, provide feedback on writing assignments, and suggest relevant sources of information to support your academic endeavors.

    No matter what your academic needs are, Assistant is here to help you achieve your goals.
    {history}
    Human: {user_input}
    Assistant:"""

    # print(os.getcwd())
    loader = PyPDFLoader('./NDTM_ANDNP.pdf')
    # loader = TextLoader('./temp.txt')
    doc = loader.load()
    # print(doc)
    # print(doc[2])
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    doc = text_splitter.split_documents(doc)

    faiss_vecstore = FAISS.from_documents(doc, OpenAIEmbeddings())

    with open("ndtmvecstore.pkl", "wb") as f:
        pickle.dump(faiss_vecstore, f)

def make_chain(vectorstore: VectorStore):
    main_llm = OpenAI(
        temperature=0.5,
        verbose=True,
    )
    from langchain.prompts.prompt import PromptTemplate
    alignment_prompt = """You will be asked theoretical computer science questions, if you are unsure of the answer say you do not know. Use the given context to the best of your abilities, do not try to make up an answer.
    {context}


    Question: {question}
    Helpful Answer:"""

    ALIGNMENT_QA_PROMPT = PromptTemplate(template=alignment_prompt, input_variables=["context", "question"])

    machine_learning_101 = LLMChain(
        llm=main_llm, prompt = ALIGNMENT_QA_PROMPT)


    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        OpenAI(temperature=0.5, verbose=True),
        # chain_type="stuff",
        # combine_documents_chain=machine_learning_101,
        retriever = vectorstore.as_retriever()
    )
    # qa_chain = VectorDBQAWithSourcesChain(
    #     vectorstore=vectorstore,
    #     #combine_documents_chain=machine_learning_101,
    # )
    load_embed_pickle()
    return qa_chain

def make_chain_prebuilt(vectorstore: VectorStore):
    qa = VectorDBQA.from_chain_type(llm=OpenAI(temperature=0.5, verbose=True), chain_type="stuff", vectorstore=vectorstore)
    query = "ndtm?"
    # qa.run(query)
    chain = load_chain("./temp.json", vectorstore=vectorstore)
    query = "How would you define the class np?"
    print(chain.run(query))

with open("ndtmvecstore.pkl", "rb") as f:
    vecstore = pickle.load(f)
    make_chain_prebuilt(vecstore)

    # split_txts = text_splitter.split_documents(doc)
    # inbedding = OpenAIEmbeddings()

    # vecstore = FAISS.from_documents(split_txts, inbedding)

    # queer = "How important is security in the cyberspace and machine learning"
    # split_txts = vecstore.similarity_search(queer)
    # print(split_txts[0])
    # print(type(split_txts))
    # print('winkis')
    # prompt = PromptTemplate(template=template, input_variables=[
    #                         "history", "user_input"])
    # chatgpt_conversation_chain = LLMChain(llm=OpenAI(temperature=0.5),
    #                                       memory=ConversationBufferWindowMemory(
    #                                           k=2),
    #                                       prompt=prompt,
    #                                       )

    # llm = OpenAI(temperature=0.5)
    # conversation_chain = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferWindowMemory())
    # # # # conversation_chain.predict(input="what is my name?")

    # history = ChatMessageHistory()
    # chat_history = ChatMessageHistory()
    # chat_history.add_user_message("")
    # chat_history.add_ai_message("")
    # conv_mem = ConversationBufferWindowMemory()
    # conv_mem.chat_memory.add_user_message("i use arch btw")
    # conv_mem.chat_memory.add_ai_message("Thats crazy")
    # print(conv_mem.load_memory_variables({}))
    # print(chat_history.messages)
    # out = ''
    # out = chatgpt_conversation_chain.predict(
        # user_input="My name is abdulla and I am from abudhabi.")
    # print(out)
    # out = chatgpt_conversation_chain.predict(user_input="What is my name?")
    # print(out)