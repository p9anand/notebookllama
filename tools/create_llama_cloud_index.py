import os
from dotenv import load_dotenv

from llama_cloud import (
    PipelineCreateEmbeddingConfig_GeminiEmbedding,
    PipelineTransformConfig_Advanced,
    AdvancedModeTransformConfigChunkingConfig_Sentence,
    AdvancedModeTransformConfigSegmentationConfig_Page,
    PipelineCreate,
)
from llama_cloud.client import LlamaCloud
from llama_index.embeddings.google import GeminiEmbedding


def main():
    load_dotenv()

    embed_model = GeminiEmbedding(
        model_name="models/embedding-001", api_key=os.getenv("GOOGLE_API_KEY")
    )

    client = LlamaCloud(token=os.getenv("LLAMACLOUD_API_KEY"))

    embedding_config = PipelineCreateEmbeddingConfig_GeminiEmbedding(
        type="GEMINI_EMBEDDING",
        component=embed_model,
    )

    segm_config = AdvancedModeTransformConfigSegmentationConfig_Page(mode="page")
    chunk_config = AdvancedModeTransformConfigChunkingConfig_Sentence(
        chunk_size=1024,
        chunk_overlap=200,
        separator="<whitespace>",
        paragraph_separator="\n\n\n",
        mode="sentence",
    )

    transform_config = PipelineTransformConfig_Advanced(
        segmentation_config=segm_config,
        chunking_config=chunk_config,
        mode="advanced",
    )

    pipeline_request = PipelineCreate(
        name="notebooklm_pipeline",
        embedding_config=embedding_config,
        transform_config=transform_config,
    )

    pipeline = client.pipelines.upsert_pipeline(request=pipeline_request)

    with open(".env", "a") as f:
        f.write(f'\nLLAMACLOUD_PIPELINE_ID="{pipeline.id}"')

    return 0


if __name__ == "__main__":
    main()
