### Classical Concentrated Solar Power Field Data

This repository contains the solar tower power field data commonly used in concentrated solar power technology research.

There are [**Gemasolar**](#Gemasolar), simulation [**6282**](#6282)  and [**PS10**](#PS10) solar field data.

##### Gemasolar  

Gemasolar is located in Andalucía, Spain, began in 2008, putted into operation in 2011.

The heliostats layout as follows:

![Gemasolar heliostat field layout](./Gemasolar/layout.png)



The layout of heliostat field references [[1]](#reference)，every position of heliostat is exported from Google Map.

Other parameters of Gemasolar  reference [[2]](#reference) and [[3]](#reference).

##### 6282

6282 is a simulation solar field in [Soltrace](https://www.nrel.gov/csp/soltrace.html) [[4]](#reference)which is not a real solar field.

The heliostats layout as follows:

![6282 simulation solar field](./6282/layout.png)

The layout of heliostat field is exported from the  example input file of Soltrace``test2.stinput``.

Other parameters is also exported in the example input file ``test2.stinput``.

By the way, the ``/6282/test2.stinput`` can be opened using the software [Soltrace](https://www.nrel.gov/csp/soltrace.html).



##### PS10

PS10 is located in Sevilla, Spain, constructed began in 2005, operation begin in 2007.

The heliostats layout as follows:

![PS10](./PS10/layout.png)

One difference from the previous two solar field is that, the receiver type of PS10 is **cavity receiver** instead of cylinder receiver. The shape of cavity receiver look like as follow [[5]](#reference):

![cavity receiver](./PS10/cavity_receiver.png)

Planform of the cavity receiver as follows:

![planform of the cavity receiver](./PS10/cavity_receiver_outline.png)

Some parameters data about PS10 can be found in [[6]](#reference),[[7]](#reference)and[[8]](#reference).

##### Reference

[1]. Sánchez-González A, Rodríguez-Sánchez M R, Santana D. Aiming strategy model based on allowable flux densities for molten salt central receivers[J]. Solar Energy, 2017, 157: 1130-1144.

[2]. Schöttl P, Moreno K O, Bern G, et al. Novel sky discretization method for optical annual assessment of solar tower plants[J]. Solar Energy, 2016, 138: 36-46.

[3]. García J, Too Y C S, Padilla R V, et al. Dynamic performance of an aiming control methodology for solar central receivers due to cloud disturbances[J]. Renewable Energy, 2018, 121: 355-367.

[4]. Wendelin T. SolTRACE: a new optical modeling tool for concentrating solar optics[C]//International solar energy conference. 2003, 36762: 253-260.

[5]. Fernández D V. PS10: a 11.0-MWe Solar Tower Power Plant with Saturated Steam Receiver[J]. Solucar.[En línea]:< www. upcomillas. es, 2004.

[6]. Osuna R, Olavarría R, Morillo R, et al. PS10, Construction of a 11MW solar thermal tower plant in Seville, Spain[C]//Proc. 13th IEA SolarPACES Symp. 2006: A4-S3.

[7]. Schöttl P, Bern G, Pretel J A F, et al. Optimization of Solar Tower molten salt cavity receivers for maximum yield based on annual performance assessment[J]. Solar Energy, 2020, 199: 278-294.

[8]. Belaid A, Filali A, Hassani S, et al. Heliostat field optimization and comparisons between biomimetic spiral and radial-staggered layouts for different heliostat shapes[J]. Solar Energy, 2022, 238: 162-177.
