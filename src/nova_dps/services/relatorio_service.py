import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.nova_dps.services.dashboard_service import DashboardService

class RelatorioPdfService:
    @staticmethod
    def gerar_relatorio_gerencial(caminho_arquivo="relatorio_gerencial_nova_dps.pdf"):
        doc = SimpleDocTemplate(
            caminho_arquivo,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        elementos = []
        estilos = getSampleStyleSheet()
        
        titulo_estilo = ParagraphStyle(
            'TituloDoc',
            parent=estilos['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0078D4'),
            spaceAfter=6
        )
        subtitulo_estilo = ParagraphStyle(
            'SubTituloDoc',
            parent=estilos['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=15
        )
        
        # Cabeçalho
        elementos.append(Paragraph("<b>NOVA DPS INFORMÁTICA</b>", titulo_estilo))
        elementos.append(Paragraph(f"Relatório Executivo e Operacional · Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", subtitulo_estilo))
        elementos.append(Spacer(1, 10))

        # Seção 1: Indicadores Chave (KPIs)
        kpis = DashboardService.obter_kpis()
        elementos.append(Paragraph("<b>1. Resumo de Indicadores e Desempenho Financeiro</b>", estilos['Heading2']))
        elementos.append(Spacer(1, 6))

        dados_kpis = [
            ["Indicador", "Valor Atual", "Meta / Referência"],
            ["Chamados Ativos em Bancada", str(kpis["pedidos_abertos"]), "≤ 15 chamados"],
            ["Total de Ordens Registradas", str(kpis["total_pedidos"]), "Crescimento contínuo"],
            ["Faturamento Bruto Acumulado", f"R$ {kpis['faturamento_total']:,.2f}", "Meta SMART: R$ 30.000/mês"],
            ["Ticket Médio por Chamado", f"R$ {kpis['ticket_medio']:,.2f}", "R$ 280,00 a R$ 450,00"],
            ["Clientes Ativos Cadastrados", str(kpis["total_clientes"]), "Meta: > 50 clientes ativos"]
        ]

        tabela_kpis = Table(dados_kpis, colWidths=[200, 160, 180])
        tabela_kpis.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ]))
        elementos.append(tabela_kpis)
        elementos.append(Spacer(1, 20))

        # Seção 2: Fila de Serviços Pendentes
        elementos.append(Paragraph("<b>2. Fila Operacional de Serviços (Ordenada por tempo de espera)</b>", estilos['Heading2']))
        elementos.append(Spacer(1, 6))

        fila = DashboardService.fila_servicos_pendentes()[:10] # Top 10 mais urgentes
        dados_fila = [["OS", "Cliente", "Equipamento", "Reparo Previsto", "Status"]]
        
        for item in fila:
            dados_fila.append([
                f"#{item['id_pedido']}",
                str(item['cliente'])[:18],
                str(item['modelo_equipamento'])[:20],
                str(item['tipo_reparo'] or 'Em triagem')[:22],
                str(item['status_servico'] or 'Aberto')
            ])

        tabela_fila = Table(dados_fila, colWidths=[40, 120, 140, 150, 90])
        tabela_fila.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F8E9')])
        ]))
        elementos.append(tabela_fila)
        elementos.append(Spacer(1, 20))

        # Rodapé Institucional
        elementos.append(Paragraph(
            "<font size=8 color='#777777'>Documento emitido automaticamente pelo Sistema de Gestão Nova DPS Informática · Projeto Integrador I - FATEC Ipiranga</font>",
            estilos['Normal']
        ))

        doc.build(elementos)
        return os.path.abspath(caminho_arquivo)
