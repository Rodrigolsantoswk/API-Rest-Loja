--CREATE DATABASE loja
USE loja

CREATE TABLE Categoria(
idCategoria			int identity,
nomeCategoria		varchar(30) not null,

constraint pk_idCategoria primary key (idCategoria));

CREATE TABLE Marca(
idMarca				int identity,
nomeMarca			varchar(30) not null,
idCategoria			int not null,

constraint fk_idCategoria foreign key(idCategoria) references Categoria(idCategoria),
constraint pk_idMarca primary key (idMarca));

CREATE TABLE Produto(
idProduto			int identity,
nomeProduto			varchar(35),
Preco				Float not null,
idMarca				int not null,

constraint fk_idMarca foreign key(idMarca) references Marca(idMarca),
constraint pk_idProduto primary key (idProduto));

CREATE TABLE Venda(
idVenda				int identity,
dtInicioVenda		datetime not null default current_timestamp,
dtFimVenda			datetime,
idCaixa				int not null,

constraint fk_idCaixa foreign key(idCaixa) references Caixa(idCaixa),
constraint pk_idVenda primary key (idVenda));

CREATE TABLE Caixa(
idCaixa				int identity,
nomeCaixa			varchar(50) not null,
dataNascimentoCaixa	date not null,
InseridoEm			datetime default current_timestamp,

constraint pk_idCaixa primary key(idCaixa));


CREATE TABLE Venda_Produto(
idVenda_Produto		int identity,
idVenda				int not null,
idProduto			int not null,

constraint fk_idVenda foreign key(idVenda) references Venda(idVenda),
constraint fk_idProduto foreign key(idProduto) references Produto(idProduto),
constraint pk_idVenda_Produto primary key (idVenda_Produto));

