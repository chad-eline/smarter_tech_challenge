import pytest

from sort import sort


class TestRejected:
    """Tests for packages that are both bulky AND heavy -> REJECTED."""

    def test_bulky_by_volume_and_heavy(self):
        assert sort(200, 200, 200, 25) == "REJECTED"

    def test_bulky_by_dimension_and_heavy(self):
        assert sort(1000, 1, 1, 30) == "REJECTED"

    def test_exactly_at_all_boundaries(self):
        # Volume = 150*150*150 = 3,375,000 (bulky), mass = 20 (heavy)
        assert sort(150, 150, 150, 20) == "REJECTED"

    def test_bulky_by_volume_exactly_and_heavy_exactly(self):
        # Volume = 100*100*100 = 1,000,000 (exactly bulky), mass = 20 (exactly heavy)
        assert sort(100, 100, 100, 20) == "REJECTED"


class TestSpecial:
    """Tests for packages that are bulky OR heavy (but not both) -> SPECIAL."""

    def test_bulky_by_dimension_not_heavy(self):
        assert sort(200, 50, 50, 10) == "SPECIAL"

    def test_heavy_not_bulky(self):
        assert sort(50, 50, 50, 25) == "SPECIAL"

    def test_bulky_by_width_only(self):
        assert sort(150, 10, 10, 5) == "SPECIAL"

    def test_bulky_by_height_only(self):
        assert sort(10, 150, 10, 5) == "SPECIAL"

    def test_bulky_by_length_only(self):
        assert sort(10, 10, 150, 5) == "SPECIAL"

    def test_bulky_by_volume_only_no_single_large_dimension(self):
        # 100 * 100 * 100 = 1,000,000 (exactly bulky by volume)
        assert sort(100, 100, 100, 19) == "SPECIAL"

    def test_exactly_heavy_not_bulky(self):
        assert sort(50, 50, 50, 20) == "SPECIAL"

    def test_exactly_bulky_by_width_not_heavy(self):
        assert sort(150, 1, 1, 19) == "SPECIAL"

    def test_exactly_bulky_by_height_not_heavy(self):
        assert sort(1, 150, 1, 19) == "SPECIAL"

    def test_exactly_bulky_by_length_not_heavy(self):
        assert sort(1, 1, 150, 19) == "SPECIAL"


class TestStandard:
    """Tests for packages that are neither bulky nor heavy -> STANDARD."""

    def test_small_and_light(self):
        assert sort(50, 50, 50, 10) == "STANDARD"

    def test_medium_size_medium_weight(self):
        # 80*80*80 = 512,000 (under 1M volume)
        assert sort(80, 80, 80, 15) == "STANDARD"

    def test_just_below_all_boundaries(self):
        # Volume = 99*99*99 = 970,299 (under 1M), each dimension < 150, mass < 20
        assert sort(99, 99, 99, 19) == "STANDARD"

    def test_minimal_package(self):
        assert sort(1, 1, 1, 1) == "STANDARD"

    def test_just_under_heavy_threshold(self):
        assert sort(50, 50, 50, 19.99) == "STANDARD"

    def test_just_under_dimension_threshold(self):
        # Each dimension under 150, volume = 99.99^3 = 999,700 (under 1M)
        assert sort(99.99, 99.99, 99.99, 19) == "STANDARD"


class TestFloatInputs:
    """Tests for floating point dimension and mass values."""

    def test_float_dimensions_standard(self):
        assert sort(50.5, 50.5, 50.5, 10.5) == "STANDARD"

    def test_float_exactly_at_heavy_boundary(self):
        assert sort(50, 50, 50, 20.0) == "SPECIAL"

    def test_float_exactly_at_dimension_boundary(self):
        assert sort(150.0, 10, 10, 5) == "SPECIAL"

    def test_float_volume_exactly_at_boundary(self):
        # 100.0 * 100.0 * 100.0 = 1,000,000.0
        assert sort(100.0, 100.0, 100.0, 19) == "SPECIAL"


class TestEdgeCases:
    """Additional edge cases and boundary conditions."""

    def test_asymmetric_dimensions_standard(self):
        # Volume = 1*1*149 = 149 (under 1M), no dimension >= 150
        assert sort(1, 1, 149, 19) == "STANDARD"

    def test_asymmetric_dimensions_bulky_by_volume(self):
        assert sort(10, 10, 10000, 19) == "SPECIAL"  # Volume = 1,000,000

    def test_very_large_single_dimension(self):
        assert sort(1000, 1, 1, 5) == "SPECIAL"  # Bulky by dimension

    def test_very_heavy_small_package(self):
        assert sort(1, 1, 1, 100) == "SPECIAL"  # Heavy only


class TestValidation:
    """Tests for input validation."""

    def test_zero_dimensions_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            sort(0, 0, 0, 1)

    def test_zero_mass_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            sort(150, 150, 150, 0)

    def test_negative_width_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            sort(-1, 10, 10, 10)

    def test_negative_height_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            sort(10, -1, 10, 10)

    def test_negative_length_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            sort(10, 10, -1, 10)

    def test_negative_mass_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            sort(10, 10, 10, -1)