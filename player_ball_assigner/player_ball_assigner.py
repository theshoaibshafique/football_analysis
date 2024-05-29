import sys
sys.path.append('../')
from utils import get_center_of_bbox,measure_distance

class PlayerBallAssigner():
    def __init__(self) -> None:
        self.max_player_ball_dist = 70

    def assign_ball_to_player(self,players,ball_bbox):
        ball_position = get_center_of_bbox(ball_bbox)

        minimum_dist = 99999
        assigned_player = -1

        for player_id,player in players.items():
            player_bbox = player['bbox']

            dist_left = measure_distance((player_bbox[0],player_bbox[-1]),ball_position)
            dist_right = measure_distance((player_bbox[2],player_bbox[-1]),ball_position)
            distance = min(dist_left,dist_right)

            if distance < self.max_player_ball_dist:
                minimum_dist=distance
                assigned_player=player_id
            
        return assigned_player