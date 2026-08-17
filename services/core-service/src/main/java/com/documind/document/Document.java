package com.documind.document;

import jakarta.persistence.*;

import java.time.Instant;

@Entity
@Table(name = "documents")
public class Document {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String tenantId;

    @Column(nullable = false)
    private String documentName;

    private String s3Key;

    private Integer chunkCount;

    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    protected Document() {
        // required by JPA
    }

    public Document(String tenantId, String documentName, String s3Key, Integer chunkCount) {
        this.tenantId = tenantId;
        this.documentName = documentName;
        this.s3Key = s3Key;
        this.chunkCount = chunkCount;
    }

    public Long getId() {
        return id;
    }

    public String getTenantId() {
        return tenantId;
    }

    public String getDocumentName() {
        return documentName;
    }

    public String getS3Key() {
        return s3Key;
    }

    public Integer getChunkCount() {
        return chunkCount;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}
