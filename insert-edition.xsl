<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs t tei"
    version="2.0">
    
    <xsl:template match="tei:body/tei:div[@type='edition']">
        <xsl:message>WARNING: this file already contains an edition div; nothing will be changed.</xsl:message>
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
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

</xsl:stylesheet>