from networkx import DiGraph
import sys
from pytest import fixture

sys.path.append("../")
sys.path.append("../vrpy/")
from vrpy.main import VehicleRoutingProblem

from examples.cvrptw_solomon import DataSet

params = list(range(2, 30))


@fixture(
    scope="class",
    params=params,
)
def n(request):
    print('setup once per each param', request.param)
    return request.param


class TestsSolomon:

    def test_subproblem(self, n):
        # benchmark result
        # e.g., in Feillet et al. (2004)
        self.data = DataSet(path="../examples/data/",
                            instance_name="c101.txt",
                            n_vertices=n)
        self.G = self.data.G
        self.data.solve()
        best_value_lp = self.data.best_value
        self.data.solve(cspy=True, exact=True)
        best_value_cspy = self.data.best_value
        assert int(best_value_lp) == int(best_value_cspy)