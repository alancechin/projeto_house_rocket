<h1 align="center">
  House Rocket - Projeto de Insights
</h1>

<h1 align="center">
  <img alt="houserocketlogo" title="#logo" src="./images/search-house.jpg" />
</h1>

## 1. Problema de Negócio
    
A House Rocket é uma empresa que realiza investimentos no mercado imobiliário. Tem por modelo de negócio realizar estudos sobre regiões onde deseja realizar operações e ter assertividade no portfólio de ativos imobiliários. Sua estratégia é comprar bons imóveis com lacuna de oportunidade de crescimento no preço para vender e obter lucros.

### 1.1 Contexto de Negócio
   O desafio no momento é iniciar operações no estado de Washington - EUA, na cidade de Seattle. Para isso, possui a disposição uma base de dados para análise que consiste em 21.613 vendas de imóveis realizadas entre as datas de 02/05/2014 à 27/05/2015 na cidade de Seattle - EUA. Essa base de dados conta com informações de venda de 21.436 imóveis distintos.

### 1.2 Questão de Negócio
   - Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?
   - Uma vez a casa comprada, qual o melhor preço para vendê-las ?

## 2. Planejamento Prévio

### 2.1 Ferramentas
  - Python 3.8
  - Mapas interativos com Plotly e Folium
  - Geopandas 
  - Jupyter Notebook
  - Spyder
  - Framework Streamlit Web Apps
  - Heroku Cloud 

### 2.2 Produto Final
   - [Página Web](https://alan-cechin-projeto-houses.herokuapp.com) contendo:
      
      - Visualização dos 5 principais insights;
      
      - Relatório com as sugestões de compra de imóveis por um valor recomendado;
      
      - Relatório com o valor recomendado de venda dos imóveis investidos.

## 3. Estudo de Negócio

De acordo com [NeighborhoodScout](https://www.neighborhoodscout.com/), dados mostram que os imóveis de Seattle - EUA se valorizaram 124,93% nos últimos dez anos, o que representa uma taxa média anual de valorização de 8,44%, colocando Seattle no top 10% nacional de valorização imobiliária.

**Fonte:** [https://www.noradarealestate.com/blog/seattle-real-estate-market/](https://www.noradarealestate.com/blog/seattle-real-estate-market/)

De acordo com diversas fontes de analistas do mercado imobiliário americano, os fatores que mais influenciam no preço dos imóveis são:
  1. Localização 
  2. Tamanho da casa e espaço útil
  3. Idade e Condição
  4. Reformas e Manutenções
  5. Oferta e Demanda
  6. Cenário Econômico

**Fontes:** 
- [https://www.mashvisor.com/blog/factors-that-affect-property-value/](https://www.mashvisor.com/blog/factors-that-affect-property-value/)

- [https://better.com/content/factors-that-impact-home-property-value/](https://better.com/content/factors-that-impact-home-property-value/)

- [https://www.homelight.com/blog/real-estate-property-value/](https://www.homelight.com/blog/real-estate-property-value/)

De acordo com [Seattle’s Mortgage Broker – Joe Tafolla](https://seattlesmortgagebroker.com/), empresa especializada em financiamento de ativos imobiliários em Seattle -EUA, o mercado possui algumas peculiaridades, como:

- O ano de construção tem uma forte influência no preço;
- A condição da propriedade pode ter um efeito significativo no financiamento da sua propriedade e quanto custa.
- O verão é a época mais popular para se mudar. Se você quiser ter o maior quantidade de imóveis para escolher, comece a pesquisar no final da primavera e início do verão. Se sua principal prioridade é fechar um acordo, o inverno é uma época melhor para comprar. O número de pessoas que compram casas é menor no inverno, então os vendedores tendem a oferecer preços mais baixos durante esse período.
- A área contruída do imóvel é um dos maiores fatores no custo de sua casa.

**Fonte:** 
- [https://seattlesmortgagebroker.com/10-secrets-to-buying-a-house-in-seattle/](https://seattlesmortgagebroker.com/10-secrets-to-buying-a-house-in-seattle/)

**EXTRA:**
- [Tendências do mercado imobiliário de Seattle para 2022 e próximos anos](https://seattleagentmagazine.com/2021/12/08/whats-the-future-of-seattle-real-estate-for-2022/)


## 4. Dados
Os dados para esse projeto foram coletados na plataforma do Kaggle: https://www.kaggle.com/harlfoxem/housesalesprediction

### 4.1 Atributos de origem

|    Atributos    |                         Definição                            |
| :-------------: | :----------------------------------------------------------: |
|       id        |           Identificação única para cada imóvel vendido
|      date       |                    Data da venda do imóvel                   |
|      price      |                 Preço que o imóvel foi vendido               |
|    bedrooms     |                      Número de quartos                       |
|    bathrooms    |                    Número de banheiros                       |
|   sqft_living   | Tamanho (em pés quadrado) do espaço interior (área construída) dos imóveis |
|    sqft_lot     |     Tamanho (em pés quadrado) do terreno onde o imóvel está situado     |
|  sqft_basement  |     Tamanho (em pés quadrado) do espaço interior que se encontra abaixo do nível do solo     |
|    sqft_above   |     Tamanho (em pés quadrado) do espaço interior que se encontra acima do nível do solo. (sqft_living - sqft_basement)     |
|     floors      |                 Número de andares do imóvel                  |
|   waterfront    |   Variável que indica a presença ou não de vista para água   |
|      view       |    Um índice de 0 a 4 de quão boa era a visão do imóvel      |
|    condition    |      Um índice de 1 a 5 que indica a condição do imóvel      |
|      grade      | Um índice de 1 a 13 que indica a qualidade da construção e o design do imóvel. |
|    yr_built     |               Ano de construção de cada imóvel               |
|  yr_renovated   |                 Ano de reforma de cada imóvel                |
|     zipcode     |                   Código Postal do imóvel                    |
|       lat       |                           Latitude                           |
|      long       |                           Longitude                          |
| sqft_livining15 | Tamanho (em pés quadrado) do espaço interno de habitação para os 15 vizinhos mais próximo |
|   sqft_lot15    | Tamanho (em pés quadrado) dos terrenos dos 15 vizinhos mais próximo |

### 4.1 Detalhamento atributos de origem

- waterfront:
    - 0 = não 
    - 1 = sim
- view:
    - 0 = Sem vista
    - 1 = Razoável
    - 2 = Média
    - 3 = Boa 
    - 4 = Excelente
- yr_renovated: 
    - 0 se nunca renovado.
- bathrooms:
    - Nos EUA existem banheiros completos contendo quatro acessórios de encanamento. Tradicionalmente, um banheiro completo contém pelo menos um lavatório(pia), uma sanitário, um chuveiro e uma banheira. Um “meio banheiro” onde 0.5 representa um banheiro com sanitário e pia mas sem chuveiro e sem banheira. 0.75 ou ¾ banho é um banheiro que contém um lavatório, um sanitário e um chuveiro ou banheira.
- condition:
    - 1 = Pobre/Desgastado. Reparação e revisão necessária em superfícies pintadas, coberturas, canalizações, aquecimento e numerosas insuficiências funcionais. Manutenção e abuso excessivos, valor em uso limitado, abandono ou reconstrução importante; reutilização ou mudança de ocupação é iminente. A idade efetiva está próxima do fim da escala, independentemente da idade cronológica real.
    - 2 = Bastante desgastado. É necessária muita reparação. Muitos itens necessitam de retoque ou revisão, manutenção diferida óbvia, utilidade de construção inadequada e sistemas, todos encurtando a esperança de vida e aumentando a idade efetiva.
    - 3 = Média. Algumas provas de manutenção diferida e obsolescência normal com a idade, na medida em que algumas pequenas reparações são necessárias, juntamente com alguns retoques. Todos os componentes principais ainda funcionam e contribuem para uma esperança de vida prolongada.
    - 4 = Bom. Não é necessária manutenção óbvia, mas também não é tudo novo. A aparência e utilidade estão acima do padrão e a idade efetiva global será mais baixa do que a propriedade típica.
    - 5= Muito Bom. Todos os artigos bem conservados, muitos dos quais foram renovados e reparados à medida que mostraram sinais de desgaste, aumentando a esperança de vida e diminuindo a idade efetiva com pouca deterioração ou obsolescência evidente com um elevado grau de utilidade.
- grade:
    - (1-3): abaixo dos padrões mínimos de construção.
    - 4: Geralmente mais antiga, construção de baixa qualidade.
    - 5: Baixos custos de construção e mão-de-obra. Projeto pequeno e simples.
    - 6: A avaliação mais baixa que cumpre atualmente o código de construção. Materiais de baixa qualidade e projeto arquitetônico simples.
    - 7: tem um nível médio de construção e concepção.
    - 8: Um pouco acima da média em construção e concepção. Normalmente melhores materiais tanto no trabalho de acabamento exterior como interior.
    - 9: Melhor design arquitetônico com design e qualidade extra no interior e exterior.
    - 10: Casas com esta qualidade têm geralmente características de alta qualidade. Os trabalhos de acabamento são melhores e mais qualidade de design é vista nas plantas dos pisos. Geralmente têm um tamanho maior.
    - 11: Desenho personalizado e trabalhos de acabamento de maior qualidade com comodidades acrescidas de madeiras maciças, instalações sanitárias e opções mais luxuosas.
    - 12: Desenho à medida e excelentes construtores. Todos os materiais são da mais alta qualidade e todas as conveniências estão presentes.
    - 13: Geralmente concebidos e construídos à medida. Nível de mansão. Grande quantidade de trabalho de armário da mais alta qualidade, acabamentos em madeira, mármore, formas de entrada, etc.


### 4.2 Fontes

- [https://www.slideshare.net/PawanShivhare1/predicting-king-county-house-prices](https://www.slideshare.net/PawanShivhare1/predicting-king-county-house-prices)

- [https://info.kingcounty.gov/assessor/esales/Glossary.aspx?type=r](https://info.kingcounty.gov/assessor/esales/Glossary.aspx?type=r)

- [https://geodacenter.github.io/data-and-lab//KingCounty-HouseSales2015/](https://geodacenter.github.io/data-and-lab//KingCounty-HouseSales2015/)


### 4.3 Atributos criados

|    Atributos    |                         Definição                            |
| :-------------: | :----------------------------------------------------------: |
|    date_str     |           Data de venda no formato Dia/Mês/Ano               |
|      month      |                    Mês da venda do imóvel                    |
|      year       |                    Ano da venda do imóvel                    |
|      age        |       Idade do imóvel. (Ano atual - Ano Construção)          |
|  is_renovated   |  Variável que indica se imóvel foi renovado (1) ou não (0)   |
|     seasons     |             Estação do ano que imóvel foi vendido            |    
|    m2_living    | Tamanho (em metros quadrados) do espaço interior (área construída) dos imóveis |
|    m2_lot       |     Tamanho (em metros quadrados) do terreno onde o imóvel está situado     |
|    m2_above     |     Tamanho (em metros quadrados) do espaço interior que se encontra acima do nível do solo     |
|   m2_outside    |     Tamanho (em metros quadrados) da área externa do terreno no imóvel     |
|  price_per_m2_living |      Preço do imóvel por metro quadrado de área construída       |
|  price_per_m2_living_outside |   Preço do imóvel por metro quadrado de área construída + área externa   |


### 4.4 Detalhamento atributos criados


- seasons:
    - Verão = de junho a agosto.
    - Outono = de setembro a novembro.
    - Inverno = de dezembro a fevereiro.
    - Primavera = de março a maio.
- m2_living, m2_lot e m2_above:
    - Converteu a unidade de medida de área dividindo o valor em pé quadrado por 10,764.
- m2_outside: 
    - Para calcular a área externa dos imóveis, subtraiu-se do tamanho de seus terrenos o valor da divisão entre a área construída acima do nível do solo sob os andares.
- price_per_m2_living:
    - Analisar o preço do imóvel tirando o impacto do tamanho de área construída dele. Preço/área construída(m2)
- price_per_m2_living_outside:
    - Analisar o preço do imóvel tirando o impacto do tamanho de área construída e a área externa. Preço/ (área construída(m2) + área externa(m2) ).
    

## 5. Premissas

- Dados Faltantes: 
    - Nenhum dos atributos do dataset possui dados faltantes
- Imóveis Duplicados:
    - Existem 177 imóveis que estão duplicados no dataset, ou seja, significa que foram vendidos mais de uma vez em períodos distintos ao longo do tempo que abrange a coleta de dados dos imóveis. Realizou-se uma análise com o intuito de compreender a variação de atributos como condição, tamanho de interior de casa ou grade entre as vendas realizadas, porém apenas o atributo "price" varia ao comparar as vendas com mesmos imóveis. 
    - Sendo assim, optou-se por manter os imóveis de forma duplicada no dataset para fins de análise de venda por período a qual as duas vendas duplicadas são importantes.
- Valor Outlier para número de quartos:
    - Encontrou-se o valor de 33 quartos informados em um determinado imóvel do dataset, avaliando a veracidade do dado buscou-se verificar o valor máximo de quartos em um imóvel abaixo dos 33 encontrados, sendo assim, existem imóveis com no máximo 11 quartos na base de dados. 
    - Além disso, analisou-se outros imóveis com faixa de preço, faixa de tamanho interno do imóvel, quantidade de banheiros e andares semelhante a esse imóvel e a quantidade média de quartos nos imóveis analisados foi de 2,98. 
    - Caso existissem os 33 quartos na casa, cada quarto ocuparia aproximadamente 50 pés quadrados tendo em vista o tamanho interno do imóvel de 1620 pés quadrados, não levando em consideração outros cômodos como cozinha e banheiro. 
    - Dessa forma, o valor de 33 será substituído por 3 assumindo possível erro de digitação.
- Imóveis com zero quartos ou zero banheiros: 
    - Existem 16 imóveis com zero quartos ou zero banheiros na base de dados, assumiremos que estão corretos e não serão excluídos dado que os imóveis podem não ter tido ainda um uso residencial. 
    - E dessa forma, devido a inexistência de banheiro ou quarto podem estar com preços descontados com relação a média dos imóveis em sua localização, sendo nesse caso possíveis oportunidades para a empresa.

## 6. Cinco Principais Insights 

   - **H1:** Imóveis com nível de condição maior ou igual a 3 são 20% mais caras, na média.
      
      ❌ **Falsa:** 
      - Considerando o **preço médio**, ao invés de 20% mais cara, são 65% mais cara.
      - Porém, se considerar o **preço médio por área construída**, são apenas 5% mais caros que os de demais condição.
      - Se acrescentarmos a **área externa** do imóvel no cálculo de preço por área, o preço de imóveis com condição maior ou igual a 3 é maior em 95% dos demais imóveis.
   
   - **H2:** Imóveis com mais de 50 anos com reforma feita são 20% mais caros, em média, que os sem reforma feita.
      
      ❌ **Falsa:** 
      - Considerando o **preço médio**, ao invés de 20% mais caras, são 53,7% mais caras.
      - Porém, se considerar o **preço médio por área construída**, são apenas 10,7% mais caros que os sem reforma feita.
   
   - **H3:** Imóveis que possuem vista para água, são 30% mais caros, na média.
      
      ❌ **Falsa:** 
      - Considerando o **preço médio**, ao invés de 30%, são 3x mais caros ou aproximadamente 212,6% mais caros, na média. 
      - Porém, se considerar o **preço médio por área construída**, imóveis que possuem vista para água são 93,7% mais caros.
      - Se acrescentarmos a **área externa** do imóvel no cálculo de preço por área, o preço de imóveis que possuem vista para água são apenas 42,7% mais caros. 
 
   
   - **H4:** Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.
      
      ❌ **Falsa:** 
      - Considerando o **preço médio**, imóveis com data de construção menor que 1955, possuem preços 0,8% mais baratos.
      - Porém, se considerar o **preço médio por área construída**, imóveis com data de construção menor que 1955 possuem preços 34,4% mais caros, na média. 
      - Se acrescentarmos a **área externa** do imóvel no cálculo de preço por área, imóveis com data de construção menor que 1955, possuem preços 22,65% mais caros, na média.  
      
   
   - **H5:** 40% das vendas de imóveis ocorrem no verão.
      
      ❌ **Falsa:** 
      - 29% dos imóveis vendidos ocorrem no verão.
      - 59% dos imóveis vendidos ocorrem no verão ou primavera.

**OBS:** Na [aplicação Web](https://alan-cechin-projeto-houses.herokuapp.com) os insights são mais aprofundados por meio de gráficos e outras análises.

## 7. Planejamento da Solução

Para responder as questões de negócio, utilizou-se pensamento analítico e análise de dados.

**Quais são os imóveis que a House Rocket deveria comprar e por qual preço** ?

1. Agrupar os imóveis por região ( zipcode ).
   - Dentro de cada região, eu vou encontrar a mediana dos preços por área construída.       
2. Vou sugerir os imóveis que:
   - Possuem preço por área construída abaixo da mediana da região e 
   - Estejam em boas condições (acima de 3) e 
   - Se Mais de 50 anos: 
      - Verificar se possui reforma feita para comprar
            
**Uma vez a casa comprada, por qual preço vendê-las**?

1. Agrupar os imóveis por região ( zipcode ) e por estação .
   - Dentro de cada região e estação, eu vou calcular a mediana do preço.
    
2. Condições de venda:
    1. Se o preço da compra por m2 for maior que a mediana da região + sazonalidade:
        - O preço da venda será igual ao preço da compra + 5% 
        - Se o grade da casa estiver acima da média da região + 5% 

    2. Se o preço da compra por m2 for menor que a mediana da região + sazonalidade. 
        - O preço da venda será igual ao preço da compra + 15%
        - Se o grade da casa estiver acima da média da região + 5% 
   
## 8. Resultados Financeiros 

Considerando todos os imóveis recomendados como compra para o investimento:


| Custo do Investimento  |   Lucro com as vendas   |   Return on Investiment (ROI) |
|------------------------|-------------------------|-------------------------|
|   $3.350.037.511,00    |    $592.827.793,05      |          17,69%         |

## 9. Conclusão

Os objetivos almejados inicialmente foram cumpridos no que tange a lista de recomendações de imóveis para compra, bem como, a projeção do valor de venda desses imóveis. Além disso, conseguiu-se obter 5 principais insights da base de dados estudada e por fim, tudo isso foi colocado em uma [aplicação na nuvem](https://alan-cechin-projeto-houses.herokuapp.com) o que facilita o acesso as análises. 

Sobre os resultados encontrados, pode-se perceber bastante influência do atributo área construída (área interna) do imóvel no preço, dessa forma, buscou-se retirar seu impacto ao comparar outros atributos com o preço para que assim, a análise não ficasse enviesada.

## 10. Próximos Passos

 Usar algoritmos de machine learning para recomendar o preço estimado de venda e compra. Usar clusterização para fazer análise de comparação de imóveis. 
 
 
