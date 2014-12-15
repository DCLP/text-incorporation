<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs t tei"
    version="2.0">
    
    <xsl:param name="input-directory"></xsl:param>
    
    <!-- capture the document element in order to:
        * test in advance for conditions relevant to processing
        * handle stylesheet behaviors accordingly -->
    <xsl:template match="tei:TEI">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:choose>
                
                <xsl:when test="//tei:body/tei:div[@type='edition']">
                    <xsl:message>WARNING: this file already contains an edition div; nothing will be changed.</xsl:message>
                    <xsl:apply-templates select="node()" mode="abort"/>
                </xsl:when>
                
                <xsl:when test="//tei:body[not(tei:div[@type='edition'])]">
                    <xsl:variable name="tm-number" select="//tei:publicationStmt/tei:idno[@type='TM'][1]"/>
                    <xsl:variable name="query">
                        <xsl:value-of select="$input-directory"/>
                        <xsl:text>/?select=</xsl:text>
                        <xsl:value-of select="$tm-number"/>
                        <xsl:text>_*.xml</xsl:text>
                    </xsl:variable>
                    <xsl:variable name="source-files" select="collection($query)"/>
                    <xsl:variable name="file-count" select="count($source-files)"/>
                    <xsl:choose>
                        <xsl:when test="$file-count=0">
                            <xsl:message>WARNING: no edition source file found for TM number <xsl:value-of select="$tm-number"/>. Nothing will be changed.</xsl:message>
                            <xsl:apply-templates select="node()" mode="abort"/>
                        </xsl:when>
                        <xsl:when test="$file-count &gt; 1">
                            <xsl:message>WARNING: multiple edition source files found for TM number <xsl:value-of select="$tm-number"/>. Nothing will be changed.</xsl:message>
                            <xsl:apply-templates select="node()" mode="abort"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:message>INFO: adding edition div</xsl:message>
                            <xsl:apply-templates select="node()">
                                <xsl:with-param name="source-file" tunnel="yes" select="$source-files[1]"/>
                            </xsl:apply-templates>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                
                <xsl:otherwise>
                    <xsl:message>WARNING: failed to find expected XML file containing text; nothing will be changed.</xsl:message>
                    <xsl:apply-templates select="node()" mode="abort"/>
                </xsl:otherwise>
                
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    

    <xsl:template match="tei:body[not(tei:div[@type='edition'])]">
        <xsl:param name="source-file" tunnel="yes"/>
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="$source-file//tei:div[@type='edition']"/>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="@*|node()" mode="abort">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" mode="abort"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>