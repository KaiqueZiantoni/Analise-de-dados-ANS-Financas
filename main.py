import sys
import time
import os


try:
    from script_ex1.ex1_1 import baixar_arquivos
    import script_ex1.ex1_2 as step1_2
    import script_ex1.ex1_3 as step1_3

    import script_ex2.ex2_1 as step2_1
    import script_ex2.ex2_2 as step2_2
    import script_ex2.ex2_3 as step2_3
    import script_ex2.gerar_zip as step_zip

except ImportError as e:
    print(f"[ERRO DE IMPORTAÇÃO] Verifique se todos os arquivos existem e não têm erros de sintaxe.")
    print(f"Detalhe do erro: {e}")
    sys.exit(1)

def main():
    print("=================================================")
    print("   INICIANDO ORQUESTRADOR DO PROJETO ANS")
    print("   Desenvolvedor: Kaique Ziantoni Rosa")
    print("=================================================\n")

    inicio_total = time.time()

    try:
        print(">>> [1/7] Executando EX1.1: Baixar Arquivos...")
        baixar_arquivos()
        print("    (Concluído)\n")

        print(">>> [2/7] Executando EX1.2: Processamento Inicial...")
        step1_2.executar() 
        print("    (Concluído)\n")

        print(">>> [3/7] Executando EX1.3: Consolidação...")
        step1_3.executar() 
        print("    (Concluído)\n")

        # --- EXECUÇÃO DA PARTE 2 ---
        print(">>> [4/7] Executando EX2.1: Transformação de Dados...")
        step2_1.executar() 
        print("    (Concluído)\n")

        print(">>> [5/7] Executando EX2.2: Enriquecimento...")
        step2_2.executar() 
        print("    (Concluído)\n")

        print(">>> [6/7] Executando EX2.3: Análises Finais...")
        step2_3.executar() 
        print("    (Concluído)\n")

        print(">>> [7/7] Gerando ZIP final para entrega...")
        step_zip.executar() 
        print("    (Concluído)\n")

        tempo_total = time.time() - inicio_total
        print("=================================================")
        print(f"   PROCESSO FINALIZADO COM SUCESSO EM {tempo_total:.2f}s")
        print("   Verifique a pasta 'output' ou 'downloads'.")
        print("=================================================")

    except AttributeError as e:
        print(f"\n[ERRO] Algum arquivo não tem a função 'executar()'.")
        print(f"Verifique se você criou 'def executar():' dentro dos arquivos.")
        print(f"Erro técnico: {e}")
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Ocorreu uma falha durante a execução: {e}")

if __name__ == "__main__":
    main()