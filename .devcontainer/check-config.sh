#!/bin/bash

# Script para verificar configurações herdadas do host
echo "🔍 Verificando configurações herdadas do host WSL..."
echo ""

# Verificar GitHub CLI
echo "📱 GitHub CLI:"
if command -v gh &> /dev/null; then
    gh auth status 2>/dev/null && echo "✅ GitHub CLI autenticado" || echo "❌ GitHub CLI não autenticado"
    echo "   Perfil ativo: $(gh auth status 2>&1 | grep -o 'Logged in to.*as.*' || echo 'Nenhum')"
else
    echo "❌ GitHub CLI não encontrado"
fi
echo ""

# Verificar Git config
echo "⚙️ Configurações Git:"
git_user=$(git config --global user.name 2>/dev/null)
git_email=$(git config --global user.email 2>/dev/null)
if [ -n "$git_user" ] && [ -n "$git_email" ]; then
    echo "✅ Git configurado: $git_user <$git_email>"
else
    echo "❌ Git não configurado globalmente"
fi

# Verificar credencial helper
cred_helper=$(git config --global credential.helper 2>/dev/null)
if [ -n "$cred_helper" ]; then
    echo "✅ Credential helper: $cred_helper"
else
    echo "⚠️  Nenhum credential helper configurado"
fi
echo ""

# Verificar SSH
echo "🔑 SSH:"
if [ -d "$HOME/.ssh" ]; then
    ssh_keys=$(ls -la ~/.ssh/*.pub 2>/dev/null | wc -l)
    if [ "$ssh_keys" -gt 0 ]; then
        echo "✅ $ssh_keys chave(s) SSH encontrada(s)"
        ls -la ~/.ssh/*.pub 2>/dev/null | awk '{print "   " $9}'
    else
        echo "⚠️  Nenhuma chave SSH pública encontrada"
    fi

    # Verificar permissões
    ssh_perms=$(stat -c "%a" ~/.ssh 2>/dev/null)
    if [ "$ssh_perms" = "700" ]; then
        echo "✅ Permissões SSH corretas (700)"
    else
        echo "⚠️  Permissões SSH incorretas: $ssh_perms (deveria ser 700)"
    fi
else
    echo "❌ Diretório SSH não encontrado"
fi
echo ""

# Verificar GPG
echo "🔐 GPG:"
if command -v gpg &> /dev/null; then
    if [ -d "$HOME/.gnupg" ]; then
        gpg_keys=$(gpg --list-secret-keys 2>/dev/null | grep -c "sec " || echo "0")
        if [ "$gpg_keys" -gt 0 ]; then
            echo "✅ $gpg_keys chave(s) GPG secreta(s) encontrada(s)"

            # Verificar chave de assinatura Git
            signing_key=$(git config --global user.signingkey 2>/dev/null)
            if [ -n "$signing_key" ]; then
                echo "✅ Chave de assinatura Git configurada: $signing_key"
            else
                echo "⚠️  Chave de assinatura Git não configurada"
            fi
        else
            echo "⚠️  Nenhuma chave GPG secreta encontrada"
        fi

        # Verificar permissões
        gnupg_perms=$(stat -c "%a" ~/.gnupg 2>/dev/null)
        if [ "$gnupg_perms" = "700" ]; then
            echo "✅ Permissões GPG corretas (700)"
        else
            echo "⚠️  Permissões GPG incorretas: $gnupg_perms (deveria ser 700)"
        fi
    else
        echo "❌ Diretório GPG não encontrado"
    fi
else
    echo "❌ GPG não instalado"
fi
echo ""

# Verificar variáveis de ambiente Git
echo "🌍 Variáveis de ambiente Git:"
for var in GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL; do
    value=$(printenv $var)
    if [ -n "$value" ]; then
        echo "✅ $var: $value"
    else
        echo "⚠️  $var não definida"
    fi
done
echo ""

# Teste de conectividade Git
echo "🌐 Teste de conectividade:"
if git ls-remote origin &>/dev/null; then
    echo "✅ Conectividade com repositório remoto funcionando"
else
    echo "❌ Problemas de conectividade com repositório remoto"
fi
echo ""

echo "🎯 Resumo:"
echo "   Para corrigir problemas de autenticação Git, execute:"
echo "   1. gh auth login (se GitHub CLI não estiver autenticado)"
echo "   2. git config --global credential.helper store (para HTTPS)"
echo "   3. git config --global user.signingkey <KEY_ID> (para assinatura GPG)"
echo ""
