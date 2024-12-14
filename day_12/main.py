file = open("./input.txt", "r")
plot_grid = file.read().split("\n")


class Region:

    def __init__(self, plot_label, first_plot_coord):
        self.plot_coords = set()
        self.plots_neighbour_coords_set = set()
        self.plots_neighbour_coords_set_with_direction = set()
        self.region_label = plot_label
        self.add_plot_to_region(first_plot_coord)

    def _compute_neighbour_coords_for_plot(self, plot_coord):
        row, col = plot_coord
        up, right, down, left = (
            (row - 1, col),
            (row, col + 1),
            (row + 1, col),
            (row, col - 1),
        )
        return [
            up,
            right,
            down,
            left,
        ]

    def add_plot_to_region(self, plot_coord):
        self.plot_coords.add(plot_coord)
        adjacent_neighbour_coords = self._compute_neighbour_coords_for_plot(plot_coord)
        self.plots_neighbour_coords_set.update(adjacent_neighbour_coords)
        for adj in adjacent_neighbour_coords:
            self.plots_neighbour_coords_set_with_direction.add((plot_coord, adj))

    def is_plot_part_of_the_region(self, plot_coord, plot_label):
        if (
            plot_label == self.region_label
            and plot_coord in self.plots_neighbour_coords_set
        ):
            return True
        return False

    def should_region_be_merged_together(self, region):
        if self == region:
            return False
        if self.region_label != region.region_label:
            return False
        if self.plot_coords.issubset(region.plot_coords):
            # We already merged the set...
            return False
        if region.plot_coords & self.plots_neighbour_coords_set:
            # The region has at least one plot adjacent to the other region
            return True
        return False

    def merge_region(self, region):
        self.plot_coords.update(region.plot_coords)
        self.plots_neighbour_coords_set.update(region.plots_neighbour_coords_set)
        self.plots_neighbour_coords_set_with_direction.update(
            region.plots_neighbour_coords_set_with_direction
        )

    def get_region_area(self):
        return len(self.plot_coords)

    def _get_coords_for_perimter_with_direction(self):
        return set(
            [
                neighbor
                for neighbor in self.plots_neighbour_coords_set_with_direction
                if neighbor[1] not in self.plot_coords
            ]
        )

    def get_region_perimeter(self):
        return len(self._get_coords_for_perimter_with_direction())

    def get_total_price_of_fencing(self):
        return self.get_region_area() * self.get_region_perimeter()

    def get_number_of_fence_sides(self):
        distinct_fence_direction = set()
        for plot_coord, adj_coord in self._get_coords_for_perimter_with_direction():
            has_another_with_same_direction = False
            for drow, dcol in [(0, 1), (1, 0)]:
                next_adj = (adj_coord[0] + drow, adj_coord[1] + dcol)
                next_plot = (plot_coord[0] + drow, plot_coord[1] + dcol)
                if (
                    next_plot,
                    next_adj,
                ) in self._get_coords_for_perimter_with_direction():
                    has_another_with_same_direction = True
            if not has_another_with_same_direction:
                distinct_fence_direction.add((plot_coord, adj_coord))
        return len(distinct_fence_direction)

    def get_total_price_of_fencing_with_discount(self):
        return self.get_region_area() * self.get_number_of_fence_sides()

    def __repr__(self):
        return str(
            "number of plot = %s required fences = %s"
            % (
                self.get_region_area(),
                self.get_region_perimeter(),
            )
        )


regions = []

for row_index, row in enumerate(plot_grid):
    for col_index, plot_label in enumerate(row):
        plot_coord = (row_index, col_index)
        try:
            matching_region = next(
                iter(
                    filter(
                        lambda r: r.is_plot_part_of_the_region(plot_coord, plot_label),
                        regions,
                    )
                )
            )
            matching_region.add_plot_to_region(plot_coord)
        except StopIteration:
            regions.append(Region(plot_label, plot_coord))

# Reconcilation step
# We could also just consider each plot its own region
# and only use the reconcilation step, but it's slower
while True:
    has_merge_region = False
    region_to_remove = set()
    for region_to_merge_into in regions:
        for region in regions:
            if region_to_merge_into.should_region_be_merged_together(region):
                has_merge_region = True
                region_to_merge_into.merge_region(region)
                region_to_remove.add(region)
        if has_merge_region:
            break
    regions = [r for r in regions if r not in region_to_remove]
    if not has_merge_region:
        break

print(
    "Result part 1 := %s" % sum(map(lambda r: r.get_total_price_of_fencing(), regions))
)

print(
    "Result part 2 := %s"
    % sum(map(lambda r: r.get_total_price_of_fencing_with_discount(), regions))
)
