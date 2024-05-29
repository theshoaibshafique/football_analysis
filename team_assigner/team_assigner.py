from sklearn.cluster import KMeans

class TeamAssigner:
    def __init__(self) -> None:
        self.team_colors = {}
        self.player_team_dict = {}


    def get_clustering_model(self,img):
        # Reshape the image to 2D Array
        img_2d = img.reshape(-1,3)

        # Perform K-means clustering with 2 clusters
        kmeans = KMeans(n_clusters=2,init="k-means++",n_init=1).fit(img_2d)

        return kmeans



    def get_player_color(self,frame,bbox):
        img = frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]

        top_img_hlf = img[0:int(img.shape[0]/2),:]

        # Get Clustering model
        kmeans = self.get_clustering_model(top_img_hlf)    

        # Get the cluster labels for each pixel
        labels = kmeans.labels_

        # Reshape the labels to original img shape
        clustered_img = labels.reshape(top_img_hlf.shape[0],top_img_hlf.shape[1])

        # Get the player cluster
        corner_clusters = [clustered_img[0,0],clustered_img[0,-1],clustered_img[-1,0],clustered_img[-1,-1]]
        np_cluster = max(set(corner_clusters),key=corner_clusters.count)
        player_cluster = 1-np_cluster

        player_color=kmeans.cluster_centers_[player_cluster]

        return player_color


    def assign_team_color(self,frame,player_detections):
        
        player_colors = []
        for _,player_detection in player_detections.items():
            bbox = player_detection['bbox']
            player_color = self.get_player_color(frame,bbox)
            player_colors.append(player_color)

        kmeans = KMeans(n_clusters=2,init='k-means++',n_init=10).fit(player_colors)
        
        self.kmeans = kmeans

        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]

    
    def get_player_team(self,frame,player_bbox,player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
        
        player_color = self.get_player_color(frame,player_bbox)

        team_id = self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id +=1

        self.player_team_dict[player_id] = team_id

        return team_id
        