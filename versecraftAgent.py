import sys
print(sys.executable)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    top_p=1.0,
    max_retries=4,
    max_tokens=200 
)

poem_prompt_template = PromptTemplate(
    input_variables=["context", "theme"],
    template="""

You are a renowned poet of the 19th century that has a great vocabaloury and a strong sense of english language .
Based on the documents provided to you construct a good poetry ,
the poetry  should not be too long and good sense of language and theme should be conveyed .  

Context:
{context}

Theme:
{theme}

Poem:
"""
)


def build_vectorstore(author_file_path, store_path):
    loader = TextLoader(author_file_path , encoding='utf-8')
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(store_path)
    print(f"Vector store saved at {store_path}")


# build_vectorstore("./data/corpus/kafka_trial.txt", "./vectorstores/kafka")
# build_vectorstore("./data/corpus/rumi.txt" , "./vectorstores/rumi")


embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vstore1 = FAISS.load_local("./vectorstores/kafka", embedding_model, allow_dangerous_deserialization=True)
vstore2 = FAISS.load_local("./vectorstores/dostovesky", embedding_model, allow_dangerous_deserialization=True)
vstore3 = FAISS.load_local("./vectorstores/rumi", embedding_model, allow_dangerous_deserialization=True)

retriever1 = vstore1.as_retriever()
retriever2 = vstore2.as_retriever()
retriever3 = vstore3.as_retriever()

# ✅ 7. Build the RetrievalQA Chain


custom_chain = LLMChain(
    llm=llm,
    prompt=poem_prompt_template
)


def generate_poem1(theme):
    try:
        docs1 = retriever1.get_relevant_documents(theme)
        


        if not docs1:
            return "⚠️ No poetic context found for that theme."

        context = "\n".join([doc.page_content for doc in docs1])
        result = custom_chain.invoke({"context": context, "theme": theme})
        return result["text"]
    except Exception as e:
        import traceback
        print("❌ ERROR in generate_poem:")
        traceback.print_exc()
        return "⚠️ Poem generation failed."


def generate_poem2(theme):
 try:
    docs2 = retriever2.get_relevant_documents(theme)
    docs3 = retriever3.get_relevant_documents(theme)


    if not docs2:
            return "⚠️ No poetic context found for that theme."

    context = "\n".join([doc.page_content for doc in docs2])
    result = custom_chain.invoke({"context": context, "theme": theme})
    return result["text"]
 

 except Exception as e:
    import traceback
    print("❌ ERROR in generate_poem:")
    traceback.print_exc()
    return "⚠️ Poem generation failed."
    


# ✅ 9. Example Run
# if __name__ == "__main__":
#     print("\n📝 Generating poem in Kafka ir dostovesky style...")
#     theme = "loneliness in the city"

#     choice = input("1 or 2 ?")
#     if choice==1:

#      result = generate_poem1(theme)
#      print("generated poem")
#      print(result)

#     else: 
#       result2 = generate_poem2(theme)
#       print("\n📜 Generated Poem:\n")
#       print(result2)

