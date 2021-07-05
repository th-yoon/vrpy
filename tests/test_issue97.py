from numpy import array
from vrpy import VehicleRoutingProblem
from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes


class TestIssue97:

    def setup(self):
        # Distance matrix
        DISTANCES = [
            [
                0, 2095.7400000000002, 1691.865516829233, 862.6229483760624,
                1601.5608041588769, 1249.374, 1578.2344525273484,
                1668.0624056689408, 1110.684, 1388.5990193830364,
                841.3631824321101, 492.1374650840197, 1184.5397511638025,
                1862.9229137819339, 1122.5363001867227, 1687.79201970507,
                1429.297, 1352.9250000000002, 1265.5129469050848,
                931.262209888035, 1446.9970000000003, 0
            ],
            [
                0, 0, 1569.7435168292332, 2372.6569483760627, 2346.338804158877,
                2759.408000000001, 3088.268452527349, 3178.0964056689418,
                2241.4875976812646, 2898.633019383037, 1285.57518243211,
                2356.3494650840207, 2954.9737511638027, 3633.6599137819335,
                2016.7367195183472, 2267.6773484827677, 3200.034,
                2829.574597681264, 1046.940946905085, 1865.058807569299,
                3253.6065976812642, 2095.7400000000007
            ],
            [
                0, 1569.7435168292332, 0, 1968.782465205296, 1561.8476358124115,
                2209.7228316535343, 2612.5582841808828, 2774.2219224981754,
                1837.6131145104976, 2348.9478510365707, 881.7006992613432,
                1952.4749819132528, 2551.0992679930364, 3229.785430611167,
                1232.245551171882, 697.9338316535344, 2796.159516829234,
                2425.7001145104973, 1305.850463734318, 1461.1843243985325,
                2849.732114510497, 1691.8655168292332
            ],
            [
                0, 2372.656948376062, 1968.7824652052955, 0, 1367.8317999868807,
                547.8209958280038, 737.6974483553521, 805.4394572928785,
                1516.7959483760626, 687.0460152110402, 1118.2801308081723,
                817.3944134600821, 610.7397469918063, 1293.480909609937,
                1027.0752485627852, 1592.3309680811326, 861.4079958280038,
                1360.0159483760626, 1542.4298952811473, 1407.6951582640975,
                1215.9829958280038, 862.6229483760626
            ],
            [
                0, 2346.3388041588764, 1561.8476358124115, 1367.8317999868807,
                0, 1165.657804158877, 1568.4932566862253, 1755.6072656237518,
                2480.716804158877, 1304.8828235419135, 1634.306986590987,
                1829.4652692428965, 1813.235206949606, 2545.8189565363064,
                550.4835236772244, 894.8578041588769, 2132.8538041588768,
                2373.2668041588777, 2058.456751063962, 2213.790611728176,
                2457.842804158877, 1601.5608041588769
            ],
            [
                0, 2759.4080000000004, 2209.7228316535347, 547.8209958280038,
                1165.657804158877, 0, 626.8304525273484, 813.9444614648747,
                2064.6169442040664, 139.22501938303637, 1505.0311824321104,
                1365.2154092880858, 871.5724027907286, 1604.1561523774294,
                1054.1913001867229, 1542.7330000000002, 1312.8429999999998,
                1907.8369442040662, 1929.1809469050854, 1949.108209888035,
                1653.9621539545312, 1249.374
            ],
            [
                0, 3088.2684525273485, 2612.558284180883, 737.6974483553521,
                1568.4932566862253, 626.8304525273484, 0, 613.4389139922231,
                2185.2496064818797, 766.0554719103848, 1833.8916349594585,
                1488.756917611368, 671.0668553180769, 1403.650604904778,
                1457.026752714071, 1945.5684525273482, 1163.3506064818794,
                2028.4696064818795, 2258.0413994324335, 2079.057662415383,
                1453.4566064818796, 1578.2344525273481
            ],
            [
                0, 3178.0964056689413, 2774.2219224981745, 805.4394572928785,
                1755.6072656237518, 813.9444614648747, 613.4389139922231, 0,
                2032.8699310851523, 953.1694808479111, 1923.7195881010512,
                1518.3283961691718, 518.6871799213496, 790.2116909125546,
                1644.1407616515976, 2132.682461464875, 1010.9709310851521,
                1876.0899310851523, 2347.8693525740264, 1940.252140973187,
                1023.831777130621, 1668.062405668941
            ],
            [
                0, 2241.487597681264, 1837.6131145104973, 1516.7959483760624,
                2480.716804158878, 2064.616944204066, 2185.2496064818797,
                2032.869931085152, 0, 2203.8419635871023, 955.9124152491543,
                1103.7514650840199, 1514.1827511638023, 1836.8009137819336,
                2001.6923001867235, 2535.5469461640314, 1386.884, 608.554,
                1411.2605445863492, 656.516209888035, 1202.097,
                1110.6840000000002
            ],
            [
                0, 2898.6330193830363, 2348.9478510365707, 687.0460152110401,
                1304.8828235419132, 139.22501938303637, 766.0554719103848,
                953.1694808479111, 2203.841963587103, 0, 1644.2562018151468,
                1504.4404286711222, 1010.797422173765, 1743.3811717604658,
                1193.4163195697593, 1681.9580193830363, 1452.0680193830362,
                2047.0619635871026, 2068.405966288122, 2088.333229271071,
                1793.1871733375674, 1388.5990193830364
            ],
            [
                0, 1285.57518243211, 881.7006992613432, 1118.2801308081725,
                1634.3069865909868, 1505.03118243211, 1833.8916349594583,
                1923.719588101051, 955.9124152491543, 1644.2562018151464, 0,
                1101.9726475161299, 1700.5969335959126, 2379.2830962140433,
                1304.7049019504573, 1579.6345309148776, 1945.65718243211,
                1543.9994152491545, 455.3481293371951, 579.4836251371892,
                1968.0314152491546, 841.3631824321101
            ],
            [
                0, 2356.349465084019, 1952.4749819132526, 817.3944134600821,
                1829.4652692428965, 1365.2154092880858, 1488.756917611368,
                1518.3283961691718, 1103.7514650840196, 1504.4404286711222,
                1101.9726475161294, 0, 999.6412162478221, 1678.327378865953,
                1350.4407652707423, 1915.6964847890897, 1244.7014650840197,
                1268.4004650840197, 1526.1224119891044, 924.3296749720547,
                1362.4724650840199, 492.13746508401965
            ],
            [
                0, 2954.9737511638023, 2551.0992679930364, 610.7397469918062,
                1813.2352069496058, 871.5724027907286, 671.0668553180769,
                518.6871799213496, 1514.1827511638025, 1010.797422173765,
                1700.5969335959126, 999.6412162478222, 0, 855.558664945736,
                1604.917051350525, 2170.1727708688722, 492.28375116380255,
                1357.4027511638026, 2124.746698068888, 1421.5649610518374,
                782.3897511638024, 1184.5397511638023
            ],
            [
                0, 3633.6599137819335, 3229.7854306111667, 1293.4809096099373,
                2545.818956536307, 1604.1561523774294, 1403.6506049047775,
                790.2116909125546, 1836.8009137819333, 1743.3811717604658,
                2379.2830962140433, 1678.3273788659533, 855.5586649457362, 0,
                2287.6582139686557, 2852.9139334870033, 1157.7129137819334,
                1680.0209137819334, 2803.4328606870185, 2089.9161236699683,
                634.7039137819336, 1862.9229137819334
            ],
            [
                0, 2016.7367195183474, 1232.245551171882, 1027.0752485627852,
                550.4835236772244, 1054.1913001867226, 1457.0267527140713,
                1644.1407616515976, 2001.692300186723, 1193.416319569759,
                1304.7049019504573, 1350.4407652707423, 1604.917051350525,
                2287.658213968656, 0, 565.2557195183474, 1855.5853001867226,
                1894.2423001867228, 1728.8546664234323, 1822.2705100747578,
                1978.8183001867228, 1122.5363001867229
            ],
            [
                0, 2267.6773484827677, 697.9338316535345, 1592.3309680811326,
                894.857804158877, 1542.733, 1945.5684525273482,
                2132.682461464875, 2535.5469461640328, 1681.9580193830363,
                1579.6345309148778, 1915.6964847890897, 2170.1727708688727,
                2852.9139334870033, 565.2557195183474, 0, 2420.84101970507,
                2459.498019705071, 2003.784295387853, 2159.1181560520668,
                2544.07401970507, 1687.79201970507
            ],
            [
                0, 3200.0340000000006, 2796.159516829234, 861.4079958280038,
                2132.853804158877, 1312.843, 1163.3506064818794,
                1010.9709310851523, 1386.8840000000002, 1452.0680193830365,
                1945.6571824321104, 1244.7014650840194, 492.28375116380255,
                1157.7129137819338, 1855.5853001867226, 2420.84101970507, 0,
                1230.1040000000003, 2369.8069469050856, 1656.2902098880352,
                718.8679999999999, 1429.297
            ],
            [
                0, 2829.5745976812636, 2425.7001145104978, 1360.0159483760622,
                2373.2668041588777, 1907.836944204066, 2028.4696064818795,
                1876.0899310851519, 608.554, 2047.0619635871024,
                1543.999415249154, 1268.4004650840195, 1357.4027511638023,
                1680.0209137819338, 1894.2423001867232, 2459.49801970507,
                1230.104, 0, 1999.3475445863492, 1244.6032098880348, 1045.317,
                1352.9249999999997
            ],
            [
                0, 1046.940946905085, 1305.850463734318, 1542.4298952811473,
                2058.456751063962, 1929.1809469050852, 2258.0413994324335,
                2347.869352574026, 1411.2605445863494, 2068.4059662881214,
                455.348129337195, 1526.1224119891042, 2124.746698068888,
                2803.4328606870185, 1728.8546664234325, 2003.7842953878524,
                2369.806946905085, 1999.3475445863496, 0, 1034.8317544743843,
                2423.379544586349, 1265.5129469050846
            ],
            [
                0, 1865.0588075692995, 1461.1843243985327, 1407.6951582640977,
                2213.7906117281764, 1949.1082098880354, 2079.057662415383,
                1940.2521409731876, 656.516209888035, 2088.3332292710716,
                579.4836251371893, 924.3296749720548, 1421.5649610518378,
                2089.9161236699692, 1822.2705100747585, 2159.118156052067,
                1656.2902098880354, 1244.603209888035, 1034.8317544743845, 0,
                1673.9902098880352, 931.2622098880352
            ],
            [
                0, 3253.606597681264, 2849.7321145104975, 1215.9829958280036,
                2457.8428041588772, 1653.9621539545315, 1453.4566064818796,
                1023.8317771306209, 1202.097, 1793.1871733375679,
                1968.031415249154, 1362.4724650840196, 782.3897511638025,
                634.7039137819335, 1978.8183001867228, 2544.07401970507,
                718.8679999999999, 1045.317, 2423.379544586349,
                1673.990209888035, 0, 1446.9969999999998
            ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Demands (key: node, value: amount)
        DEMAND = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 1,
            12: 1,
            13: 1,
            14: 1,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 1
        }

        # The matrix is transformed into a DiGraph
        A = array(DISTANCES, dtype=[("cost", int)])
        self.G = from_numpy_matrix(A, create_using=DiGraph())
        # The demands are stored as node attributes
        set_node_attributes(self.G, values=DEMAND, name="demand")
        # The depot is relabeled as Source and Sink
        self.G = relabel_nodes(self.G, {0: "Source", 21: "Sink"})
        self.prob = VehicleRoutingProblem(self.G, load_capacity=5)
        self.prob.num_vehicles = 5
        self.prob.use_all_vehicles = True

    def test_cspy(self):
        self.prob.solve()
        assert (self.prob.best_value == 22749)

    def test_lp(self):
        # This takes a few seconds (close to 9)
        self.prob.solve(cspy=False)
        assert (self.prob.best_value == 22749)
