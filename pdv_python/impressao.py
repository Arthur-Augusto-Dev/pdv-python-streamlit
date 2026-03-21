import win32print
import win32ui

def imprimir_na_termica(texto_cupom):
    printer_name = win32print.GetDefaultPrinter()
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        # Cria o job de impressão
        print_job = win32print.StartDocPrinter(hPrinter, 1, ("Cupom PDV", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        
        # Envia o texto convertido para bytes
        win32print.WritePrinter(hPrinter, texto_cupom.encode('utf-8'))
        
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)
