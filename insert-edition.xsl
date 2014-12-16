<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs t tei"
    version="2.0">
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    <xsl:param name="input-directory">.</xsl:param>
    <xsl:param name="who">Ghost in the Machine</xsl:param>
    <xsl:param name="overwrite">no</xsl:param>
    
    <!-- capture the document element in order to:
        * test in advance for conditions relevant to processing
        * handle stylesheet behaviors accordingly -->
    <xsl:template match="tei:TEI">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:choose>
                
                <xsl:when test="//tei:body/tei:div[@type='edition']">
                    <xsl:message>INFO: this file already contains an edition div!</xsl:message>
                    <xsl:choose>
                        <xsl:when test="$overwrite='yes'">
                            <xsl:message>INFO: the "overwrite" parameter is set to "yes", so the existing edition div will be replaced with the new one from the corresponding input file.</xsl:message>
                            <xsl:call-template name="insert-edition"/>
                        </xsl:when>
                        <xsl:when test="$overwrite='no'">
                            <xsl:message>INFO: the "overwrite" parameter is set to "no", so the edition div will not be replaced.</xsl:message>
                            <xsl:apply-templates select="node()" mode="abort"/>
                        </xsl:when>
                    </xsl:choose>
                </xsl:when>
                
                <xsl:when test="//tei:body[not(tei:div[@type='edition'])]">
                    <xsl:message>INFO: no edition div was found, so the external edition div will be brought in.</xsl:message>
                    <xsl:call-template name="insert-edition"/>
                </xsl:when>
                
                <xsl:otherwise>
                    <xsl:message>WARNING: unexpected structure in file. Nothing will be changed.</xsl:message>
                    <xsl:apply-templates select="node()" mode="abort"/>
                </xsl:otherwise>
                
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template name="insert-edition">
        <xsl:variable name="tm-number" select="//tei:publicationStmt/tei:idno[@type='TM'][1]"/>
        <xsl:variable name="query">
            <xsl:value-of select="$input-directory"/>
            <xsl:text>/?select=</xsl:text>
            <xsl:value-of select="$tm-number"/>
            <xsl:text>.xml</xsl:text>
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
                <xsl:message>INFO: adding edition div from external file</xsl:message>
                <xsl:apply-templates select="node()">
                    <xsl:with-param name="source-file" tunnel="yes" select="$source-files[1]"/>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:body">
        <xsl:param name="source-file" tunnel="yes"/>
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="$source-file//tei:div[@type='edition']"/>
            <xsl:apply-templates select="tei:div[@type!='edition']"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="tei:revisionDesc">
        <xsl:param name="source-file" tunnel="yes"/>
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:text>
        </xsl:text>
            <change when="{current-dateTime()}" who="{$who}">Programmatically incorporated edition div and associated revision description into document</change>
            <xsl:for-each select="$source-file//tei:revisionDesc/* | *">
                <xsl:sort select="xs:date(@when)" order="descending" />
                <xsl:text> 
        </xsl:text>
                <xsl:apply-templates select="."/>
            </xsl:for-each>
            <xsl:text>
      </xsl:text>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="text()[parent::tei:change]">
        <xsl:value-of select="normalize-space()"/>
        <xsl:if test="contains(normalize-space(), 'Crosswalked to EpiDoc XML')">
            <xsl:choose>
                <xsl:when test="./ancestor::tei:TEI/descendant::tei:div[@type='edition']">
                    <xsl:text> (edition div)</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text> (metadata)</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
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