"""Create a ChatVectorDBChain for question/answering."""
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import (CONDENSE_QUESTION_PROMPT)
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores.base import VectorStore

from custom_prompts import FIELD_PROMPT
from custom_prompts import SOLUTION_PROMPT


def get_chain(
    vectorstore: VectorStore, question_handler, stream_handler, tracing: bool = False, first: bool = False
) -> ConversationalRetrievalChain:
    """Create a ChatVectorDBChain for question/answering."""
    # Construct a ChatVectorDBChain with a streaming llm for combine docs
    # and a separate, non-streaming llm for question generation
    manager = AsyncCallbackManager([])
    question_manager = AsyncCallbackManager([question_handler])
    stream_manager = AsyncCallbackManager([stream_handler])
    if tracing:
        tracer = LangChainTracer()
        tracer.load_default_session()
        manager.add_handler(tracer)
        question_manager.add_handler(tracer)
        stream_manager.add_handler(tracer)

    question_gen_llm = OpenAI(
        temperature=0,
        verbose=True,
        callback_manager=question_manager,
    )
    streaming_llm = OpenAI(
        streaming=True,
        callback_manager=stream_manager,
        verbose=True,
        temperature=0,
        max_tokens=512
    )

    custom_prompt = FIELD_PROMPT
    if first:
        custom_prompt = SOLUTION_PROMPT

    question_generator = LLMChain(
        llm=streaming_llm, prompt=custom_prompt, callback_manager=manager
    )

    return question_generator
    # doc_chain = load_qa_chain(
    #         streaming_llm, chain_type="stuff", prompt=custom_prompt, callback_manager=manager
    #     )
    # memory = ConversationKGMemory(llm=streaming_llm, memory_key="chat_history", output_key='answer')
    #
    # qa = ConversationalRetrievalChain(  # <==CHANGE  ConversationalRetrievalChain instead of ChatVectorDBChain
    #     retriever=vectorstore.as_retriever(),
    #     combine_docs_chain=doc_chain,
    #     question_generator=question_generator,
    #     callback_manager=manager,
    #     # memory=memory,
    #     verbose=True,
    #     return_source_documents=True,
    #     # get_chat_history=lambda h : h
    # )

    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=streaming_llm,
    #     retriever=vectorstore.as_retriever(),
    #     # memory=memory,
    #     return_source_documents=True,
    #     # get_chat_history=lambda h :h,
    #     combine_docs_chain_kwargs={'prompt': custom_prompt} #use custom prompt if one needs customisation.
# )


    return qa
