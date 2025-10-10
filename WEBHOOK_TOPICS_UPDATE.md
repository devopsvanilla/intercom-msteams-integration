# Atualização dos Tópicos de Webhook do Intercom

## Resumo das Correções

Baseado na análise da documentação oficial do Intercom (https://developers.intercom.com/docs/references/webhooks/webhook-models#section-webhook-topics), identificamos e corrigimos os seguintes problemas na configuração de webhooks:

## ❌ Tópicos Incorretos (que não existem)

Os seguintes tópicos mencionados na documentação não existem na API do Intercom:

- `user.signed_up` ❌
- `contact.created` ❌
- `contact.signed_up` ❌

## ✅ Tópicos Corretos Implementados

### Eventos de Conversação (já funcionavam corretamente)
- `conversation.user.created` - Nova conversa criada por usuário
- `conversation.user.replied` - Usuário respondeu à conversa
- `conversation.admin.replied` - Admin respondeu à conversa
- `conversation.admin.assigned` - Conversa atribuída a admin
- `conversation.admin.closed` - Conversa fechada por admin

### Eventos de Contato (novos handlers adicionados)
- `contact.user.created` - Novo contato usuário criado
- `contact.lead.created` - Novo lead criado
- `contact.lead.signed_up` - Lead convertido em usuário
- `visitor.signed_up` - Visitante convertido em usuário

## 🔧 Mudanças Implementadas

### 1. Webhook Handler (`webhook_handler.py`)
- ✅ Adicionados 4 novos handlers para eventos de contato
- ✅ Corrigida verificação de assinatura de SHA-256 para SHA-1 (conforme especificação do Intercom)
- ✅ Mensagens específicas para cada tipo de evento de contato

### 2. Documentação Atualizada
- ✅ `README-intercom-setup.md` - Corrigidos tópicos de webhook
- ✅ `README.md` - Listados todos os eventos suportados
- ✅ Exemplos de teste curl atualizados com SHA-1

### 3. Testes
- ✅ Adicionados testes para todos os novos handlers de webhook
- ✅ Corrigida verificação de assinatura nos testes para usar SHA-1
- ✅ Todos os testes passando

## 📝 Configuração no Intercom

Para configurar os webhooks no Intercom, use os seguintes tópicos:

### Eventos Essenciais
```
conversation.user.created
conversation.user.replied
conversation.admin.replied
conversation.admin.assigned
conversation.admin.closed
```

### Eventos de Contato (opcional)
```
contact.user.created
contact.lead.created
contact.lead.signed_up
visitor.signed_up
```

## 🔒 Verificação de Assinatura

**IMPORTANTE**: O Intercom usa SHA-1 para assinatura de webhooks, não SHA-256.

- Header: `X-Hub-Signature: sha1=<hash>`
- Algoritmo: HMAC-SHA1
- Chave: Client Secret do seu app Intercom

## 🧪 Testando os Webhooks

Use os exemplos em `README-intercom-setup.md` com o header correto:

```bash
curl -X POST https://seu-webhook-url/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature: sha1=<hash-calculado>" \
  -d '{"topic": "contact.user.created", "data": {...}}'
```

## 📊 Benefícios

1. **Conformidade**: Agora usando apenas tópicos que existem na API do Intercom
2. **Cobertura Completa**: Suporte para todos os eventos relevantes de contato
3. **Segurança**: Verificação correta de assinatura usando SHA-1
4. **Notificações Ricas**: Mensagens específicas no Teams para cada tipo de evento
5. **Testes Abrangentes**: Cobertura de teste para todos os handlers

## 🚀 Próximos Passos

1. Atualizar a configuração de webhook no Intercom para usar os tópicos corretos
2. Testar os novos eventos em ambiente de desenvolvimento
3. Monitorar logs para verificar funcionamento correto
4. Considerar adicionar eventos adicionais conforme necessidade (ver documentação oficial)
