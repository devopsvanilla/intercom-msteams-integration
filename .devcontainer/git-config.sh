#!/bin/bash

# Configurações do Git para o Dev Container
# Este script resolve o problema de variáveis de ambiente vazias do Git

echo "🔧 Configurando Git para o Dev Container..."
echo ""

# Verificar se já existe configuração
current_name=$(git config --get user.name 2>/dev/null)
current_email=$(git config --get user.email 2>/dev/null)

if [[ -n "$current_name" && -n "$current_email" ]]; then
    echo "📋 Configuração atual do Git:"
    echo "   Nome: $current_name"
    echo "   Email: $current_email"
    echo ""
    echo "Deseja manter essa configuração? (s/N)"
    read -r keep_config
    if [[ "$keep_config" =~ ^[SsYy]$ ]]; then
        export GIT_AUTHOR_NAME="$current_name"
        export GIT_AUTHOR_EMAIL="$current_email"
        export GIT_COMMITTER_NAME="$current_name"
        export GIT_COMMITTER_EMAIL="$current_email"
        echo "✅ Configuração mantida!"
        exit 0
    fi
fi

# Solicitar nome do usuário
echo "👤 Configure suas informações do Git:"
while true; do
    echo -n "Digite seu nome completo: "
    read -r user_name
    if [[ -n "$user_name" ]]; then
        break
    fi
    echo "❌ Nome não pode estar vazio!"
done

# Solicitar email do usuário
while true; do
    echo -n "Digite seu email: "
    read -r user_email
    if [[ -n "$user_email" && "$user_email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        break
    fi
    if [[ -z "$user_email" ]]; then
        echo "❌ Email não pode estar vazio!"
    else
        echo "❌ Email inválido! Use o formato: nome@dominio.com"
    fi
done

echo ""
echo "📝 Configurações que serão aplicadas:"
echo "   Nome: $user_name"
echo "   Email: $user_email"
echo ""
echo "Confirma essas configurações? (S/n)"
read -r confirm
if [[ "$confirm" =~ ^[Nn]$ ]]; then
    echo "❌ Configuração cancelada!"
    exit 1
fi

# Definir variáveis de ambiente do Git
export GIT_AUTHOR_NAME="$user_name"
export GIT_AUTHOR_EMAIL="$user_email"
export GIT_COMMITTER_NAME="$user_name"
export GIT_COMMITTER_EMAIL="$user_email"

# Configurar Git localmente
git config user.name "$user_name"
git config user.email "$user_email"

echo ""
echo "✅ Git configurado com sucesso!"
echo "   Nome: $(git config --get user.name)"
echo "   Email: $(git config --get user.email)"
echo ""
echo "💡 Dica: Essas configurações serão mantidas para esta sessão do container."
echo "   Execute este script novamente se precisar reconfigurar."
