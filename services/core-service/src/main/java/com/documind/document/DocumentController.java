package com.documind.document;

import com.documind.auth.tenant.TenantContext;
import jakarta.validation.Valid;
import org.springframework.http.ResponseStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Document metadata for the current tenant. Actual file bytes and vector
 * chunks live in S3 / the rag-service's Postgres+pgvector store — this
 * service only owns metadata, tenant scoping, and auth, so a query here
 * never crosses into another tenant's documents.
 */
@RestController
@RequestMapping("/documents")
public class DocumentController {

    private final DocumentRepository documentRepository;

    public DocumentController(DocumentRepository documentRepository) {
        this.documentRepository = documentRepository;
    }

    @PostMapping
    @ResponseStatus(org.springframework.http.HttpStatus.CREATED)
    public Document register(@Valid @RequestBody RegisterDocumentRequest request) {
        String tenantId = TenantContext.getTenantId();
        Document document = new Document(tenantId, request.documentName(), request.s3Key(), request.chunkCount());
        return documentRepository.save(document);
    }

    @GetMapping
    public List<Document> listForCurrentTenant() {
        String tenantId = TenantContext.getTenantId();
        return documentRepository.findByTenantId(tenantId);
    }
}
