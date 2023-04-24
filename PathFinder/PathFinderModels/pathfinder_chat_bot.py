import os, pickle
from langchain import OpenAI, LLMChain, VectorDBQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores import VectorStore
from langchain.chains import RetrievalQAWithSourcesChain, VectorDBQAWithSourcesChain, load_chain
from langchain.memory import ConversationBufferWindowMemory, ChatMessageHistory

from langchain.vectorstores.pgvector import PGVectorStore


template = """Assistant is a LLM trained by OpenAI.
Assistant is a language model designed to assist with academic questions and provide guidance as an academic mentor/tutor. With a vast knowledge base and the ability to process natural language, Assistant can answer questions on a wide range of subjects, including but not limited to, law, economics, history, science, mathematics, and literature.

As an academic mentor/tutor, Assistant can provide guidance on study habits, essay writing, research methodologies, and exam preparation. Whether you are a high school student, college student, or graduate student, Assistant is equipped to provide the support and guidance you need to succeed academically.

With its advanced capabilities, Assistant can also help you generate ideas for research projects, provide feedback on writing assignments, and suggest relevant sources of information to support your academic endeavors.

No matter what your academic needs are, Assistant is here to help you achieve your goals.
{history}
Human: {user_input}
Assistant:"""

# api_key = os.environ.get('OPENAI_API_KEY')


# TODO: langchain has a prebuild QAchain -> VectorDBQA.from_chain_type(llm...)
def load_embed_pickle() -> None:

    # print(os.getcwd())
    loader = PyPDFLoader('./NDTM_ANDNP.pdf')
    # loader = TextLoader('./temp.txt')
    doc = loader.load()
    # print(doc)
    # print(doc[2])
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)
    doc = text_splitter.split_documents(doc)

    # faiss_vecstore = FAISS.from_documents(doc, OpenAIEmbeddings())

    # if not os.path.exists("ndtmvecstore.pkl"):
        # with open("ndtmvecstore.pkl", "wb") as f:
            # pickle.dump(faiss_vecstore, f)
    # print(len(doc))
    # print(doc[0].page_content)


def make_chain(vectorstore: VectorStore) -> RetrievalQAWithSourcesChain:
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
    # load_embed_pickle()
    return qa_chain

def make_chain_prebuilt(vectorstore: VectorStore) -> str:
    # qa = VectorDBQA.from_chain_type(llm=OpenAI(temperature=0.5, verbose=True), chain_type="stuff", vectorstore=vectorstore)
    # query = "ndtm?"
    # qa.run(query)
    # llm = OpenAI(temperature=0, verbose=True)
    chain = load_chain("./temp.json", vectorstore=vectorstore)
    query = "How would you define the class np? explain it like im 4 years old"
    docs = vectorstore.similarity_search(query)
    return chain.run(input=docs, query=query)
    # print(chain.run(query))
