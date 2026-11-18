from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.metadata.openapi import OpenApiTags
from drf_spectacular.types import OpenApiTypes

from django.core.cache import cache

import hashlib
import json

# =========================
# LANGCHAIN / OLLAMA
# =========================
from langchain_community.llms import Ollama 
from langchain_core.prompts import PromptTemplate

# =========================
# VECTOR DATABASE
# =========================
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

# =========================
# IMPORT DATA SOURCES
# =========================
from .active_trading_codes import (
    get_admin_realtime_turnover_comaparison_sector_wise,
    get_admin_realtime_turnover_comaparison_top20_sector_wise,
    get_active_trading_summary,
    get_admin_oms_branch_wise_turnover_dt_as_on_month
)

from .rmwise_daily_trade_performance import (
    get_rmwise_daily_trade_date
)

# =========================
# LLM INIT
# =========================
llm = Ollama(
    model="llama3",
    temperature=0.2
)

# =========================
# EMBEDDING MODEL
# =========================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# VECTOR DATABASE
# =========================
vector_db = Chroma(
    collection_name="financial_analysis",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)

# =========================
# DETECT DATA TYPE
# =========================
def detect_data_type(prompt: str):

    p = prompt.lower()

    branch_keywords = [
        "branch",
        "branch-wise"
    ]

    sector_keywords = [
        "sector",
        "sector-wise"
    ]

    company_keywords = [
        "company",
        "companies",
        "stock"
    ]

    summary_keywords = [
        "summary",
        "trading",
        "clients",
        "channel",
        "total",
        "dt",
        "internet"
    ]

    counts = {
        "branch_turnover": sum(k in p for k in branch_keywords),
        "sector": sum(k in p for k in sector_keywords),
        "company": sum(k in p for k in company_keywords),
        "summary": sum(k in p for k in summary_keywords),
    }

    if max(counts.values()) == 0:
        return "summary"

    return max(counts, key=counts.get)

# =========================
# DETECT TURNOVER TYPE
# =========================
def detect_turnover_type(prompt: str):

    p = prompt.lower()

    dse_keywords = [
        "dse",
        "dse turnover",
        "dse turover"
    ]

    lbsl_keywords = [
        "lbsl",
        "lbsl turnover",
        "lbs",
        "lbsl turover"
    ]

    both_keywords = [
        "both",
        "combined",
        "total",
        "all"
    ]

    dse = any(k in p for k in dse_keywords)
    lbsl = any(k in p for k in lbsl_keywords)
    both = any(k in p for k in both_keywords)

    if both or (dse and lbsl):
        return "both"

    if dse:
        return "dse"

    if lbsl:
        return "lbsl"

    return "dse"

# =========================
# FETCH DATA
# =========================
def fetch_data_by_type(request, data_type):

    try:

        if data_type == "sector":

            res = get_admin_realtime_turnover_comaparison_sector_wise(
                request._request
            )

            return res.data if res.status_code == 200 else None

        elif data_type == "company":

            res = get_admin_realtime_turnover_comaparison_top20_sector_wise(
                request._request
            )

            return res.data if res.status_code == 200 else None

        elif data_type == "branch_turnover":

         res = get_admin_oms_branch_wise_turnover_dt_as_on_month(
         request._request
         )

        if res.status_code == 200:
            rows = res.data.get("rows", [])

            formatted_rows = [
            {
                "branch_Name": row.get("branch_Name"),
                "active_clients_today": row.get("active_clients_today"),
                "turnover_today": row.get("turnover_today"),
            }
            for row in rows
            ]
            return formatted_rows

        elif data_type == "summary":

            res = get_active_trading_summary(
                request._request
            )

            return res.data if res.status_code == 200 else None

    except Exception as e:
        print("FETCH ERROR:", str(e))
        return None

# =========================
# CLEAN SECTOR DATA
# =========================
def clean_sector_data(data, turnover_type="dse"):

    cleaned = []

    for item in data:

        cleaned.append({
            "sector": item.get("name"),
            "dse_turnover": round(
                item.get("DSE_turnover", 0), 2
            ),
            "lbsl_turnover": round(
                item.get("LBSL_turnover", 0), 2
            ),
        })

    def sort_key(x):

        if turnover_type == "dse":
            return x["dse_turnover"]

        elif turnover_type == "lbsl":
            return x["lbsl_turnover"]

        return (
            x["dse_turnover"] +
            x["lbsl_turnover"]
        )

    cleaned = sorted(
        cleaned,
        key=sort_key,
        reverse=True
    )

    return cleaned[:10]

# =========================
# CLEAN COMPANY DATA
# =========================
def clean_company_data(data, turnover_type="dse"):

    cleaned = []

    for item in data:

        cleaned.append({
            "company": item.get("name"),
            "sector": item.get("sector"),
            "dse_turnover": round(
                item.get("DSE_turnover", 0), 2
            ),
            "lbsl_turnover": round(
                item.get("LBSL_turnover", 0), 2
            ),
        })

    def sort_key(x):

        if turnover_type == "dse":
            return x["dse_turnover"]

        elif turnover_type == "lbsl":
            return x["lbsl_turnover"]

        return (
            x["dse_turnover"] +
            x["lbsl_turnover"]
        )

    cleaned = sorted(
        cleaned,
        key=sort_key,
        reverse=True
    )

    return cleaned[:20]

# =========================
# GENERIC CLEANER
# =========================
def clean_data(data, config):

    if not isinstance(data, list):
        return data

    limit = config.get("limit", 10)

    cleaned = []

    for item in data:

        if not isinstance(item, dict):
            continue

        new_item = {
            k: (
                round(v, 2)
                if isinstance(v, (int, float))
                else v
            )
            for k, v in item.items()
        }

        new_item = {
            k: v
            for k, v in new_item.items()
            if v is not None
        }

        cleaned.append(new_item)

    return cleaned[:limit]

# =========================
# CLEAN CONFIG
# =========================
def get_clean_config(data_type):

    return {
        "sector": {"limit": 10},
        "company": {"limit": 20},
        "branch_turnover": {"limit": 10},
        "summary": {"limit": 10},
    }.get(data_type, {"limit": 10})

# =========================
# VECTOR DOCUMENTS
# =========================
def convert_to_documents(data, data_type):

    documents = []

    for i, item in enumerate(data):

        content = json.dumps(item)

        doc = Document(
            page_content=content,
            metadata={
                "data_type": data_type,
                "index": i
            }
        )

        documents.append(doc)

    return documents

# =========================
# PROMPT
# =========================
def build_prompt(data_type):

    context_map = {
        "sector": "Sector-wise market analysis",
        "company": "Top company performance analysis",
        "branch_turnover": "Branch-wise performance",
        "summary": "Trading summary"
    }

    context = context_map.get(
        data_type,
        "Financial analysis"
    )

    template = """
You are a professional financial analyst.

Context:
{context}

Turnover Type:
{turnover_type}

Historical Similar Financial Data:
{retrieved_context}

Latest Financial Data:
{data}

User Question:
{question}

Rules:
- Use ONLY provided data
- Compare DSE and LBSL if available
- Do NOT create fake values
- Always use BDT (৳)
- Give concise insights
"""

    return (
        PromptTemplate.from_template(template),
        context
    )

# =========================
# MAIN API
# =========================
@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "prompt",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY
        )
    ],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def ask(request):

    prompt = request.query_params.get(
        "prompt",
        "Give summary"
    )

    # =========================
    # DETECT TYPES
    # =========================
    data_type = detect_data_type(prompt)

    turnover_type = detect_turnover_type(
        prompt
    )

    # =========================
    # FETCH DATA
    # =========================
    data = fetch_data_by_type(
        request,
        data_type
    )

    ##print("Fetched Data:", data)

    if not data:

        return Response({
            "error": "No data",
            "status": "failed"
        }, status=400)

    # =========================
    # CLEAN DATA
    # =========================
    config = get_clean_config(data_type)

    if data_type == "sector":

        data = clean_sector_data(
            data,
            turnover_type
        )

    elif data_type == "company":

        data = clean_company_data(
            data,
            turnover_type
        )

    else:

        data = clean_data(
            data,
            config
        )

    # =========================
    # STORE VECTOR DATA
    # =========================
    documents = convert_to_documents(
        data,
        data_type
    )

    try:

        vector_db.add_documents(
            documents=documents,
            ids=[
                f"{data_type}_{turnover_type}_{i}"
                for i in range(len(documents))
            ]
        )

    except Exception as e:
        print("VECTOR STORE ERROR:", str(e))

    # =========================
    # VECTOR SEARCH
    # =========================
    try:

        retrieved_docs = vector_db.similarity_search(
            prompt,
            k=5
        )

        retrieved_context = "\n".join([
            doc.page_content
            for doc in retrieved_docs
        ])

    except Exception as e:

        print("VECTOR SEARCH ERROR:", str(e))
        retrieved_context = ""

    # =========================
    # CACHE
    # =========================
    cache_key = (
        f"{data_type}_"
        f"{turnover_type}_"
        f"{hashlib.md5(prompt.encode()).hexdigest()}"
    )

    cached = cache.get(cache_key)

    if cached:

        return Response({
            "question": prompt,
            "data_type": data_type,
            "turnover_type": turnover_type,
            "answer": cached,
            "cached": True,
            "status": "success"
        })

    # =========================
    # LLM
    # =========================
    prompt_template, context = build_prompt(
        data_type
    )

    chain = prompt_template | llm

    try:

        answer = chain.invoke({
            "context": context,
            "data": json.dumps(data),
            "question": prompt,
            "turnover_type": turnover_type,
            "retrieved_context": retrieved_context
        })

        if hasattr(answer, "content"):
            answer = answer.content

        # =========================
        # CACHE SAVE
        # =========================
        cache.set(
            cache_key,
            answer,
            600 
        )

        return Response({
            "question": prompt,
            "data_type": data_type,
            "turnover_type": turnover_type,
            "retrieved_context": retrieved_context,
            "answer": answer,
            "cached": False,
            "status": "success"
        })

    except Exception as e:

        return Response({
            "error": str(e),
            "status": "failed"
        }, status=500)