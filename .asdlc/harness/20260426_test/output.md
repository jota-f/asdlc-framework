```python
"""
Testes para Calculadora
Autor: Test Agent
Data: 2025-03-26
Versão: 1.0
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Any, Dict, List
import logging

# Importar módulo a ser testado
from calculadora import Calculadora

# Configurar logging para testes
logger = logging.getLogger(__name__)

class TestCalculadora:
    """
    Testes unitários para a classe Calculadora
    """
    
    @pytest.fixture
    def instance(self):
        """Fixture para criar instância da classe"""
        return Calculadora()
    
    def test_init_default_values(self, instance):
        """
        Testa inicialização com valores padrão
        """
        # Arrange
        expected_operacoes = []
        
        # Act
        # (instance já criada no fixture)
        
        # Assert
        assert instance.historico == expected_operacoes
    
    def test_somar_positivos(self, instance):
        """
        Testa soma de dois números positivos
        """
        # Arrange
        a, b = 3, 5
        expected_result = 8
        
        # Act
        result = instance.somar(a, b)
        
        # Assert
        assert result == expected_result
    
    def test_somar_negativos(self, instance):
        """
        Testa soma de números negativos
        """
        assert instance.somar(-2, -3) == -5
    
    def test_subtrair(self, instance):
        """
        Testa subtração
        """
        assert instance.subtrair(10, 4) == 6
    
    def test_multiplicar(self, instance):
        """
        Testa multiplicação
        """
        assert instance.multiplicar(3, 4) == 12
    
    def test_dividir_positivos(self, instance):
        """
        Testa divisão exata
        """
        assert instance.dividir(10, 2) == 5.0
    
    def test_dividir_por_zero(self, instance):
        """
        Testa divisão por zero
        """
        with pytest.raises(ValueError, match="Divisão por zero não permitida"):
            instance.dividir(5, 0)
    
    def test_registra_historico(self, instance):
        """
        Testa se o histórico é registrado após operação
        """
        instance.somar(1, 2)
        assert len(instance.historico) == 1
        assert instance.historico[0] == "1 + 2 = 3"
    
    @pytest.mark.parametrize("a,b,esperado", [
        (0, 0, 0),
        (100, 0, 100),
        (-5, 10, 5),
        (1.5, 2.5, 4.0),
    ])
    def test_somar_parametrized(self, instance, a, b, esperado):
        """
        Testa soma com diferentes entradas
        """
        assert instance.somar(a, b) == esperado
    
    def test_obter_ultimo_resultado_vazio(self, instance):
        """
        Testa obter último resultado sem histórico
        """
        assert instance.obter_ultimo_resultado() is None
    
    def test_obter_ultimo_resultado_com_historico(self, instance):
        """
        Testa obter último resultado após operação
        """
        instance.somar(3, 7)
        assert instance.obter_ultimo_resultado() == 10

class TestCalculadoraIntegracao:
    """
    Testes de integração para Calculadora
    """
    
    def test_calculo_composto(self):
        """
        Testa sequência de operações
        """
        calc = Calculadora()
        resultado = calc.somar(10, 20)
        resultado = calc.subtrair(resultado, 5)
        resultado = calc.multiplicar(resultado, 2)
        assert resultado == 50

# Testes de performance (exemplo)
class TestCalculadoraPerformance:
    """
    Testes de performance para Calculadora
    """
    
    def test_somar_performance(self, benchmark):
        """
        Testa performance da soma
        """
        calc = Calculadora()
        result = benchmark(calc.somar, 999999, 1)
        assert result == 1000000

# Configuração do pytest (para testes lentos)
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
```