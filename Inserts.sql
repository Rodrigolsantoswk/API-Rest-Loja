
  INSERT INTO Categoria values
  ('Limpeza'),
  ('Higiene'),
  ('Lanches'),
  ('Condimentos'),
  ('Bebidas'),
  ('Frutas')


  INSERT INTO Caixa values
  ('Rodrigo', CAST('1999-09-25' AS DATE), current_timestamp),
  ('Yuri', CAST('1997-02-03' AS DATE), current_Timestamp),
  ('Alice', CAST('2000-01-23' AS DATE), current_timestamp)

  INSERT INTO Marca
  VALUES
  ('Colgate', 2),
  ('Maria', 3),
  ('Coca-Cola', 5),
  ('Marca de vassoura', 1),
  ('Marca de pano', 1)


  INSERT INTO Produto values
  ('Creme dental P', 1, 2.90),
  ('Biscoito', 2, 4.40),
  ('Refrigerante 2L', 3, 5.40),
  ('Refrigerante 1L', 3, 3.40),
  ('Vassoura', 4, 5.35),
  ('Pano', 5, 2.10)


  INSERT INTO Venda VALUES
  (CAST('21-10-2021 19:21:00' AS Datetime), CAST('21-10-2021 19:22:00' AS Datetime), 1),
  (CAST('21-10-2021 15:13:00' AS Datetime), CAST('21-10-2021 15:25:00' AS Datetime), 2),
  (CAST('21-10-2021 09:14:00' AS Datetime), CAST('21-10-2021 09:15:00' AS Datetime), 1),
  (CAST('21-10-2021  14:18:00' AS Datetime), CAST('21-10-2021 14:22:00' AS Datetime), 3)

  INSERT INTO Venda_Produto VALUES
  (4, 1),
  (4, 1),
  (4, 2),
  (5, 3),
  (6, 5),
  (6, 4),
  (7, 6)

  SELECT * FROM Venda
  SELECT * FROM produto
  SELECT * FROM Venda_Produto
  SELECT * FROM Caixa