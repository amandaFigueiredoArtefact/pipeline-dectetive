CREATE TABLE analise.resumo_pedidos AS
SELECT
    p.id_pedido,
    p.data_pedido,
    c.nome_cliente,
    SUM(p.valor) AS valor_total_pedido,
    MAX(pg.data_pagamento) AS ultimo_pagamento
FROM
    bruto.pedidos AS p
JOIN
    bruto.clientes AS c ON p.id_cliente = c.id_cliente
LEFT JOIN
    bruto.pagamentos AS pg ON p.id_pedido = pg.id_pedido
WHERE
    p.status = 'entregue'
GROUP BY
    1, 2, 3;