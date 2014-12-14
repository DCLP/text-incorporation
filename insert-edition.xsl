<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs t tei"
    version="2.0">
    
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
                    <!-- TODO: test for existence of file to insert and load it into a tunnel parameter -->
                    <xsl:message>INFO: adding edition div</xsl:message>
                    <xsl:apply-templates select="node()"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:message>WARNING: failed to find expected XML file containing text; nothing will be changed.</xsl:message>
                    <xsl:apply-templates select="node()" mode="abort"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    

    <xsl:template match="tei:body[not(tei:div[@type='edition'])]">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <div type="edition">
                <ab>hi I'm a new baby edition!</ab>
            </div>
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