import numpy as np

Q_TABLE = {(4, 1, False): np.array([-0.32261974, -0.3221752 ]),
(4, 2, False): np.array([-0.10914523, -0.09945101]),
(4, 3, False): np.array([-0.09511619, -0.06530075]),
(4, 4, False): np.array([-0.0926355 , -0.03867409]),
(4, 5, False): np.array([-0.06261647, -0.02359545]),
(4, 6, False): np.array([-0.09065094,  0.00386549]),
(4, 7, False): np.array([-0.17908258, -0.08121296]),
(4, 8, False): np.array([-0.20270213, -0.12304115]),
(4, 9, False): np.array([-0.23441722, -0.18857565]),
(4, 10, False): np.array([-0.50718037, -0.3083289 ]),
(5, 1, False): np.array([-0.4962133 , -0.41919003]),
(5, 2, False): np.array([-0.16281989, -0.11574712]),
(5, 3, False): np.array([-0.16908707, -0.09771133]),
(5, 4, False): np.array([-0.1268698 , -0.05716348]),
(5, 5, False): np.array([-0.11179588, -0.02347392]),
(5, 6, False): np.array([-0.13451618, -0.01001852]),
(5, 7, False): np.array([-0.28220421, -0.12543336]),
(5, 8, False): np.array([-0.33224143, -0.17678296]),
(5, 9, False): np.array([-0.36622624, -0.2451265 ]),
(5, 10, False): np.array([-0.58764964, -0.33972126]),
(6, 1, False): np.array([-0.61617659, -0.44710266]),
(6, 2, False): np.array([-0.21023987, -0.13802534]),
(6, 3, False): np.array([-0.22443665, -0.10199099]),
(6, 4, False): np.array([-0.16026766, -0.06448285]),
(6, 5, False): np.array([-0.12910989, -0.03684575]),
(6, 6, False): np.array([-0.09240888, -0.01250579]),
(6, 7, False): np.array([-0.37957272, -0.15015257]),
(6, 8, False): np.array([-0.41497612, -0.21631378]),
(6, 9, False): np.array([-0.45109207, -0.28800829]),
(6, 10, False): np.array([-0.60207952, -0.35301742]),
(7, 1, False): np.array([-0.67511824, -0.46100062]),
(7, 2, False): np.array([-0.22910068, -0.1035343 ]),
(7, 3, False): np.array([-0.19875841, -0.07457247]),
(7, 4, False): np.array([-0.19072769, -0.03637827]),
(7, 5, False): np.array([-0.17814629, -0.01439585]),
(7, 6, False): np.array([-0.14685507,  0.03498784]),
(7, 7, False): np.array([-0.41038252, -0.07090274]),
(7, 8, False): np.array([-0.46009084, -0.21634968]),
(7, 9, False): np.array([-0.49129866, -0.27354512]),
(7, 10, False): np.array([-0.55389229, -0.33938135]),
(8, 1, False): np.array([-0.72097436, -0.39226036]),
(8, 2, False): np.array([-0.30428863, -0.02515523]),
(8, 3, False): np.array([-0.28694554,  0.0193446 ]),
(8, 4, False): np.array([-0.23157687,  0.03248362]),
(8, 5, False): np.array([-0.1469198,  0.074894 ]),
(8, 6, False): np.array([-0.16464924,  0.1060251 ]),
(8, 7, False): np.array([-0.4331737 ,  0.06472674]),
(8, 8, False): np.array([-0.46642154, -0.06008891]),
(8, 9, False): np.array([-0.50822459, -0.19854009]),
(8, 10, False): np.array([-0.54023034, -0.28669745]),
(9, 1, False): np.array([-0.78058703, -0.31570303]),
(9, 2, False): np.array([-0.29444435,  0.06774432]),
(9, 3, False): np.array([-0.19689593,  0.10953983]),
(9, 4, False): np.array([-0.22203506,  0.12431532]),
(9, 5, False): np.array([-0.14239752,  0.14256871]),
(9, 6, False): np.array([-0.14552455,  0.18994973]),
(9, 7, False): np.array([-0.44042676,  0.18306338]),
(9, 8, False): np.array([-0.50132474,  0.09110209]),
(9, 9, False): np.array([-0.53424341, -0.04199371]),
(9, 10, False): np.array([-0.61203111, -0.2075975 ]),
(10, 1, False): np.array([-0.75376409, -0.18973785]),
(10, 2, False): np.array([-0.27931102,  0.15795026]),
(10, 3, False): np.array([-0.22745626,  0.21116957]),
(10, 4, False): np.array([-0.18311916,  0.24094936]),
(10, 5, False): np.array([-0.1568065 ,  0.24899889]),
(10, 6, False): np.array([-0.12066539,  0.28845695]),
(10, 7, False): np.array([-0.47521956,  0.25489745]),
(10, 8, False): np.array([-0.52528456,  0.17988832]),
(10, 9, False): np.array([-0.56258491,  0.11195583]),
(10, 10, False): np.array([-0.56008122, -0.02299258]),
(11, 1, False): np.array([-0.77465075, -0.08849545]),
(11, 2, False): np.array([-0.30377457,  0.23535492]),
(11, 3, False): np.array([-0.24458115,  0.24625499]),
(11, 4, False): np.array([-0.20689586,  0.27627012]),
(11, 5, False): np.array([-0.19297622,  0.2816549 ]),
(11, 6, False): np.array([-0.11524071,  0.31089842]),
(11, 7, False): np.array([-0.45567604,  0.26394693]),
(11, 8, False): np.array([-0.50629533,  0.20953424]),
(11, 9, False): np.array([-0.5504394 ,  0.12374554]),
(11, 10, False): np.array([-0.57022265,  0.05022978]),
(12, 1, False): np.array([-0.77166268, -0.51439922]),
(12, 1, True): np.array([-0.32175096, -0.17205404]),
(12, 2, False): np.array([-0.28064819, -0.25176672]),
(12, 2, True): np.array([-0.11570383,  0.05534787]),
(12, 3, False): np.array([-0.27355763, -0.24199935]),
(12, 3, True): np.array([-0.11546187,  0.07178178]),
(12, 4, False): np.array([-0.240467  , -0.23075381]),
(12, 4, True): np.array([-0.10776138,  0.08586951]),
(12, 5, False): np.array([-0.19748907, -0.22165597]),
(12, 5, True): np.array([-0.06613176,  0.10608478]),
(12, 6, False): np.array([-0.21510727, -0.20099622]),
(12, 6, True): np.array([-0.05873035,  0.12679388]),
(12, 7, False): np.array([-0.46646455, -0.20118421]),
(12, 7, True): np.array([-0.16856384,  0.12276408]),
(12, 8, False): np.array([-0.50878894, -0.2655795 ]),
(12, 8, True): np.array([-0.20136156,  0.05920912]),
(12, 9, False): np.array([-0.56874942, -0.34066735]),
(12, 9, True): np.array([-0.23442184,  0.00309251]),
(12, 10, False): np.array([-0.57184708, -0.41300575]),
(12, 10, True): np.array([-0.51920247, -0.11638536]),
(13, 1, False): np.array([-0.77588732, -0.5350984 ]),
(13, 1, True): np.array([-0.51628011, -0.23516102]),
(13, 2, False): np.array([-0.31512471, -0.32201469]),
(13, 2, True): np.array([-0.21251357,  0.05907507]),
(13, 3, False): np.array([-0.25190747, -0.29754946]),
(13, 3, True): np.array([-0.16524224,  0.06874649]),
(13, 4, False): np.array([-0.19171227, -0.27345631]),
(13, 4, True): np.array([-0.12692267,  0.09424047]),
(13, 5, False): np.array([-0.18824875, -0.27376717]),
(13, 5, True): np.array([-0.13844187,  0.12003197]),
(13, 6, False): np.array([-0.18050931, -0.25668893]),
(13, 6, True): np.array([-0.08077055,  0.15302208]),
(13, 7, False): np.array([-0.4704655 , -0.28914515]),
(13, 7, True): np.array([-0.33780927,  0.11098279]),
(13, 8, False): np.array([-0.51697998, -0.32069711]),
(13, 8, True): np.array([-0.34014567,  0.03899962]),
(13, 9, False): np.array([-0.54749164, -0.36420155]),
(13, 9, True): np.array([-0.36570341, -0.02073518]),
(13, 10, False): np.array([-0.58186542, -0.46695205]),
(13, 10, True): np.array([-0.5745688 , -0.13294926]),
(14, 1, False): np.array([-0.76951404, -0.5727121 ]),
(14, 1, True): np.array([-0.50595429, -0.29139847]),
(14, 2, False): np.array([-0.28830669, -0.34347246]),
(14, 2, True): np.array([-0.18565225,  0.02021637]),
(14, 3, False): np.array([-0.25220438, -0.35391426]),
(14, 3, True): np.array([-0.16882513,  0.05482954]),
(14, 4, False): np.array([-0.21680743, -0.35144212]),
(14, 4, True): np.array([-0.15610984,  0.08105383]),
(14, 5, False): np.array([-0.15878853, -0.31837519]),
(14, 5, True): np.array([-0.11121288,  0.09508916]),
(14, 6, False): np.array([-0.14165548, -0.32778712]),
(14, 6, True): np.array([-0.10866329,  0.13173739]),
(14, 7, False): np.array([-0.45337839, -0.30796953]),
(14, 7, True): np.array([-0.33695421,  0.07771571]),
(14, 8, False): np.array([-0.54167509, -0.36360511]),
(14, 8, True): np.array([-0.33627941,  0.0056672 ]),
(14, 9, False): np.array([-0.56349177, -0.43303724]),
(14, 9, True): np.array([-0.35386101, -0.07300546]),
(14, 10, False): np.array([-0.59395322, -0.4943381 ]),
(14, 10, True): np.array([-0.58190287, -0.1800522 ]),
(15, 1, False): np.array([-0.77212948, -0.6285821 ]),
(15, 1, True): np.array([-0.56227994, -0.32371342]),
(15, 2, False): np.array([-0.29789132, -0.43847929]),
(15, 2, True): np.array([-0.20479501,  0.0099157 ]),
(15, 3, False): np.array([-0.25409627, -0.4223479 ]),
(15, 3, True): np.array([-0.15818441,  0.02416261]),
(15, 4, False): np.array([-0.24445896, -0.42914865]),
(15, 4, True): np.array([-0.13142449,  0.06090862]),
(15, 5, False): np.array([-0.2066561 , -0.37995317]),
(15, 5, True): np.array([-0.16590609,  0.09300604]),
(15, 6, False): np.array([-0.15944903, -0.38151521]),
(15, 6, True): np.array([-0.08549094,  0.11090065]),
(15, 7, False): np.array([-0.49813824, -0.35124793]),
(15, 7, True): np.array([-0.3374726 ,  0.02506587]),
(15, 8, False): np.array([-0.53174844, -0.44237551]),
(15, 8, True): np.array([-0.35092075, -0.03167505]),
(15, 9, False): np.array([-0.52826387, -0.44498813]),
(15, 9, True): np.array([-0.35567051, -0.10888126]),
(15, 10, False): np.array([-0.57288021, -0.54979827]),
(15, 10, True): np.array([-0.56524867, -0.22618715]),
(16, 1, False): np.array([-0.75668474, -0.65058909]),
(16, 1, True): np.array([-0.54068237, -0.35971455]),
(16, 2, False): np.array([-0.3042756 , -0.51001288]),
(16, 2, True): np.array([-0.21271352, -0.04005632]),
(16, 3, False): np.array([-0.24025226, -0.48991796]),
(16, 3, True): np.array([-0.15190693,  0.01797181]),
(16, 4, False): np.array([-0.22600717, -0.50221927]),
(16, 4, True): np.array([-0.17570665,  0.04292239]),
(16, 5, False): np.array([-0.16209718, -0.42627459]),
(16, 5, True): np.array([-0.14738178,  0.08570208]),
(16, 6, False): np.array([-0.15925013, -0.44568474]),
(16, 6, True): np.array([-0.12459329,  0.1141114 ]),
(16, 7, False): np.array([-0.45398823, -0.43230067]),
(16, 7, True): np.array([-0.33412674,  0.01180292]),
(16, 8, False): np.array([-0.53277517, -0.4802607 ]),
(16, 8, True): np.array([-0.38255346, -0.06128114]),
(16, 9, False): np.array([-0.55403351, -0.50610579]),
(16, 9, True): np.array([-0.38004943, -0.15406515]),
(16, 10, False): np.array([-0.61023953, -0.58466692]),
(16, 10, True): np.array([-0.59517253, -0.24780529]),
(17, 1, False): np.array([-0.62079468, -0.67975468]),
(17, 1, True): np.array([-0.49765627, -0.37377825]),
(17, 2, False): np.array([-0.14496377, -0.54714174]),
(17, 2, True): np.array([-0.10994475, -0.01685352]),
(17, 3, False): np.array([-0.11368791, -0.54088671]),
(17, 3, True): np.array([-0.09129132,  0.02100329]),
(17, 4, False): np.array([-0.09134803, -0.56295647]),
(17, 4, True): np.array([-0.09669858,  0.05648373]),
(17, 5, False): np.array([-0.04679583, -0.50266088]),
(17, 5, True): np.array([-0.0309709,  0.1030203]),
(17, 6, False): np.array([ 0.00482471, -0.5112369 ]),
(17, 6, True): np.array([0.03400735, 0.13550947]),
(17, 7, False): np.array([-0.0678911 , -0.49222281]),
(17, 7, True): np.array([-0.07412442,  0.06321345]),
(17, 8, False): np.array([-0.39681942, -0.51171808]),
(17, 8, True): np.array([-0.28429302, -0.07041392]),
(17, 9, False): np.array([-0.42988097, -0.54539263]),
(17, 9, True): np.array([-0.32337267, -0.14256666]),
(17, 10, False): np.array([-0.45083866, -0.59946028]),
(17, 10, True): np.array([-0.45132937, -0.23461504]),
(18, 1, False): np.array([-0.34114002, -0.72201638]),
(18, 1, True): np.array([-0.31446674, -0.30098989]),
(18, 2, False): np.array([ 0.14371622, -0.63749271]),
(18, 2, True): np.array([0.09747287, 0.02244312]),
(18, 3, False): np.array([ 0.16391773, -0.62712593]),
(18, 3, True): np.array([0.13315043, 0.0312467 ]),
(18, 4, False): np.array([ 0.1658437 , -0.63354478]),
(18, 4, True): np.array([0.19359456, 0.05788246]),
(18, 5, False): np.array([ 0.20133954, -0.61534517]),
(18, 5, True): np.array([0.21483602, 0.08349812]),
(18, 6, False): np.array([ 0.28986177, -0.64287505]),
(18, 6, True): np.array([0.29749246, 0.09328153]),
(18, 7, False): np.array([ 0.39122377, -0.60119807]),
(18, 7, True): np.array([0.35875036, 0.10136988]),
(18, 8, False): np.array([ 0.10705056, -0.58021902]),
(18, 8, True): np.array([0.09499305, 0.00032427]),
(18, 9, False): np.array([-0.18469958, -0.63548851]),
(18, 9, True): np.array([-0.14113314, -0.09619656]),
(18, 10, False): np.array([-0.25666681, -0.69490011]),
(18, 10, True): np.array([-0.2339352 , -0.18829614]),
(19, 1, False): np.array([-0.12557076, -0.77304557]),
(19, 1, True): np.array([-0.11897898, -0.1933037 ]),
(19, 2, False): np.array([ 0.39782057, -0.7475292 ]),
(19, 2, True): np.array([0.38016347, 0.08353336]),
(19, 3, False): np.array([ 0.41329649, -0.7316121 ]),
(19, 3, True): np.array([0.37466563, 0.08673438]),
(19, 4, False): np.array([ 0.42747388, -0.72945743]),
(19, 4, True): np.array([0.43860382, 0.11131091]),
(19, 5, False): np.array([ 0.43470614, -0.69539915]),
(19, 5, True): np.array([0.42419712, 0.12617909]),
(19, 6, False): np.array([ 0.47510043, -0.7147594 ]),
(19, 6, True): np.array([0.49772146, 0.14288014]),
(19, 7, False): np.array([ 0.61890101, -0.70892131]),
(19, 7, True): np.array([0.62460311, 0.1282801 ]),
(19, 8, False): np.array([ 0.59811524, -0.73647472]),
(19, 8, True): np.array([0.59224007, 0.08863226]),
(19, 9, False): np.array([ 0.3005032 , -0.71254289]),
(19, 9, True): np.array([ 0.29592161, -0.01410271]),
(19, 10, False): np.array([-0.02144191, -0.73896345]),
(19, 10, True): np.array([-0.04494159, -0.155252  ]),
(20, 1, False): np.array([ 0.14539007, -0.88084753]),
(20, 1, True): np.array([ 0.16465213, -0.14496665]),
(20, 2, False): np.array([ 0.64094083, -0.84485991]),
(20, 2, True): np.array([0.62090873, 0.1268409 ]),
(20, 3, False): np.array([ 0.66474301, -0.85574817]),
(20, 3, True): np.array([0.63759979, 0.13897635]),
(20, 4, False): np.array([ 0.67514894, -0.85031358]),
(20, 4, True): np.array([0.66602794, 0.16825332]),
(20, 5, False): np.array([ 0.65824388, -0.84702948]),
(20, 5, True): np.array([0.66852035, 0.19844795]),
(20, 6, False): np.array([ 0.68804956, -0.86599254]),
(20, 6, True): np.array([0.6971803 , 0.19506536]),
(20, 7, False): np.array([ 0.7836892 , -0.85914026]),
(20, 7, True): np.array([0.78554068, 0.18688801]),
(20, 8, False): np.array([ 0.77232082, -0.85074552]),
(20, 8, True): np.array([0.79748408, 0.14087773]),
(20, 9, False): np.array([ 0.75896594, -0.8634467 ]),
(20, 9, True): np.array([0.7792373 , 0.10789046]),
(20, 10, False): np.array([ 0.4364491 , -0.87059709]),
(20, 10, True): np.array([ 0.43487674, -0.06786446]),
(21, 1, False): np.array([ 0.63745899, -0.98970697]),
(21, 1, True): np.array([ 0.68147839, -0.10075697]),
(21, 2, False): np.array([ 0.87663419, -0.98757686]),
(21, 2, True): np.array([0.97725235, 0.21234139]),
(21, 3, False): np.array([ 0.88705266, -0.98670225]),
(21, 3, True): np.array([0.98337094, 0.25769685]),
(21, 4, False): np.array([ 0.88154966, -0.98755198]),
(21, 4, True): np.array([0.97922585, 0.26144027]),
(21, 5, False): np.array([ 0.89617896, -0.98828897]),
(21, 5, True): np.array([0.9830878 , 0.28297946]),
(21, 6, False): np.array([ 0.90503146, -0.98675536]),
(21, 6, True): np.array([0.98169051, 0.29114249]),
(21, 7, False): np.array([ 0.91710404, -0.99000133]),
(21, 7, True): np.array([0.98232238, 0.28177945]),
(21, 8, False): np.array([ 0.93638517, -0.99166585]),
(21, 8, True): np.array([0.98742039, 0.24129021]),
(21, 9, False): np.array([ 0.9334075, -0.9892006]),
(21, 9, True): np.array([0.9874354 , 0.14904215]),
(21, 10, False): np.array([ 0.89375429, -0.99999999]),
(21, 10, True): np.array([0.91659469, 0.03083558]),
(22, 1, False): np.array([0., 0.]),
(22, 2, False): np.array([0., 0.]),
(22, 3, False): np.array([0., 0.]),
(22, 4, False): np.array([0., 0.]),
(22, 5, False): np.array([0., 0.]),
(22, 6, False): np.array([0., 0.]),
(22, 7, False): np.array([0., 0.]),
(22, 8, False): np.array([0., 0.]),
(22, 9, False): np.array([0., 0.]),
(22, 10, False): np.array([0., 0.]),
(23, 1, False): np.array([0., 0.]),
(23, 2, False): np.array([0., 0.]),
(23, 3, False): np.array([0., 0.]),
(23, 4, False): np.array([0., 0.]),
(23, 5, False): np.array([0., 0.]),
(23, 6, False): np.array([0., 0.]),
(23, 7, False): np.array([0., 0.]),
(23, 8, False): np.array([0., 0.]),
(23, 9, False): np.array([0., 0.]),
(23, 10, False): np.array([0., 0.]),
(24, 1, False): np.array([0., 0.]),
(24, 2, False): np.array([0., 0.]),
(24, 3, False): np.array([0., 0.]),
(24, 4, False): np.array([0., 0.]),
(24, 5, False): np.array([0., 0.]),
(24, 6, False): np.array([0., 0.]),
(24, 7, False): np.array([0., 0.]),
(24, 8, False): np.array([0., 0.]),
(24, 9, False): np.array([0., 0.]),
(24, 10, False): np.array([0., 0.]),
(25, 1, False): np.array([0., 0.]),
(25, 2, False): np.array([0., 0.]),
(25, 3, False): np.array([0., 0.]),
(25, 4, False): np.array([0., 0.]),
(25, 5, False): np.array([0., 0.]),
(25, 6, False): np.array([0., 0.]),
(25, 7, False): np.array([0., 0.]),
(25, 8, False): np.array([0., 0.]),
(25, 9, False): np.array([0., 0.]),
(25, 10, False): np.array([0., 0.]),
(26, 1, False): np.array([0., 0.]),
(26, 2, False): np.array([0., 0.]),
(26, 3, False): np.array([0., 0.]),
(26, 4, False): np.array([0., 0.]),
(26, 5, False): np.array([0., 0.]),
(26, 6, False): np.array([0., 0.]),
(26, 7, False): np.array([0., 0.]),
(26, 8, False): np.array([0., 0.]),
(26, 9, False): np.array([0., 0.]),
(26, 10, False): np.array([0., 0.]),
(27, 1, False): np.array([0., 0.]),
(27, 2, False): np.array([0., 0.]),
(27, 3, False): np.array([0., 0.]),
(27, 4, False): np.array([0., 0.]),
(27, 5, False): np.array([0., 0.]),
(27, 6, False): np.array([0., 0.]),
(27, 7, False): np.array([0., 0.]),
(27, 8, False): np.array([0., 0.]),
(27, 9, False): np.array([0., 0.]),
(27, 10, False): np.array([0., 0.]),
(28, 1, False): np.array([0., 0.]),
(28, 2, False): np.array([0., 0.]),
(28, 3, False): np.array([0., 0.]),
(28, 4, False): np.array([0., 0.]),
(28, 5, False): np.array([0., 0.]),
(28, 6, False): np.array([0., 0.]),
(28, 7, False): np.array([0., 0.]),
(28, 8, False): np.array([0., 0.]),
(28, 9, False): np.array([0., 0.]),
(28, 10, False): np.array([0., 0.]),
(29, 1, False): np.array([0., 0.]),
(29, 2, False): np.array([0., 0.]),
(29, 3, False): np.array([0., 0.]),
(29, 4, False): np.array([0., 0.]),
(29, 5, False): np.array([0., 0.]),
(29, 6, False): np.array([0., 0.]),
(29, 7, False): np.array([0., 0.]),
(29, 8, False): np.array([0., 0.]),
(29, 9, False): np.array([0., 0.]),
(29, 10, False): np.array([0., 0.]),
(30, 1, False): np.array([0., 0.]),
(30, 2, False): np.array([0., 0.]),
(30, 3, False): np.array([0., 0.]),
(30, 4, False): np.array([0., 0.]),
(30, 5, False): np.array([0., 0.]),
(30, 6, False): np.array([0., 0.]),
(30, 7, False): np.array([0., 0.]),
(30, 8, False): np.array([0., 0.]),
(30, 9, False): np.array([0., 0.]),
(30, 10, False): np.array([0., 0.]),
(31, 1, False): np.array([0., 0.]),
(31, 2, False): np.array([0., 0.]),
(31, 3, False): np.array([0., 0.]),
(31, 4, False): np.array([0., 0.]),
(31, 5, False): np.array([0., 0.]),
(31, 6, False): np.array([0., 0.]),
(31, 7, False): np.array([0., 0.]),
(31, 8, False): np.array([0., 0.]),
(31, 9, False): np.array([0., 0.]),
(31, 10, False): np.array([0., 0.])}