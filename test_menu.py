#!/usr/bin/env python3
"""
Script de teste para verificar o menu interativo
"""
import sys
from io import StringIO
from unittest.mock import patch

def test_menu_choice_3():
    """Testa a opção 3 do menu (criar story)"""
    from asdlc.ui_manager import UIManager
    
    ui = UIManager()
    
    # Simular entrada do usuário
    with patch('builtins.input', side_effect=['3', 'Teste de Story via Menu', '0']):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            try:
                ui.start_interactive_mode()
                output = fake_output.getvalue()
                print("✅ Teste concluído!")
                print("Output capturado:")
                print(output)
            except Exception as e:
                print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    test_menu_choice_3() 