package com.documind.document;

import jakarta.validation.constraints.NotBlank;

public record RegisterDocumentRequest(
        @NotBlank String documentName,
        String s3Key,
        Integer chunkCount
) {}
