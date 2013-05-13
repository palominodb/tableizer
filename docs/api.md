# Tableizer API Documentation

Tableizer provides a browseable API. To view this, simply follow the steps below.

1. Run the development server

        ./manage.py runserver

2. Visit the browsable API url using your browser

        Example URL: http://127.0.0.1:8000/api/v1/

## Sample API Usage

1. Get all servers

        curl http://localhost:8000/api/v1/servers/
        
        [
            {
                "url": "http://localhost:8000/api/v1/servers/1/", 
                "databases": [
                    2, 
                    8, 
                    4, 
                    9, 
                    3, 
                    7, 
                    5, 
                    6, 
                    1
                ], 
                "id": 1, 
                "name": "localhost", 
                "cached_size": 217038848, 
                "created_at": "2013-05-03T13:53:44", 
                "updated_at": "2013-05-13T18:00:09"
            }
        ]

2. Get specific server

        curl http://localhost:8000/api/v1/servers/1/
        
        {
            "databases": [
                {
                    "url": "http://localhost:8000/api/v1/databases/2/", 
                    "tables": [
                        47, 
                        48, 
                        43, 
                        46, 
                        44, 
                        41, 
                        42, 
                        45
                    ], 
                    "id": 2, 
                    "name": "employees", 
                    "server": 1, 
                    "cached_size": 205979648, 
                    "created_at": "2013-05-03T13:53:44", 
                    "updated_at": "2013-05-13T18:00:09"
                }, 
                {
                    "url": "http://localhost:8000/api/v1/databases/8/", 
                    "tables": [
                        143, 
                        138, 
                        134, 
                        141, 
                        140, 
                        128, 
                        129, 
                        125, 
                        136, 
                        126, 
                        132, 
                        131, 
                        127, 
                        137, 
                        124, 
                        133, 
                        130, 
                        139, 
                        142, 
                        135
                    ], 
                    "id": 8, 
                    "name": "tableizer", 
                    "server": 1, 
                    "cached_size": 6651904, 
                    "created_at": "2013-05-03T13:53:45", 
                    "updated_at": "2013-05-13T18:00:09"
                }, 
            ],
            "id": 1, 
            "name": "localhost", 
            "cached_size": 217038848, 
            "created_at": "2013-05-03T13:53:44", 
            "updated_at": "2013-05-13T18:00:09"
        }
        
3. Get all databses

        curl http://localhost:8000/api/v1/databases/
        
        [
            {
                "url": "http://localhost:8000/api/v1/databases/2/", 
                "tables": [
                    47, 
                    48, 
                    43, 
                    46, 
                    44, 
                    41, 
                    42, 
                    45
                ], 
                "id": 2, 
                "name": "employees", 
                "server": 1, 
                "cached_size": 205979648, 
                "created_at": "2013-05-03T13:53:44", 
                "updated_at": "2013-05-13T18:00:09"
            }, 
            {
                "url": "http://localhost:8000/api/v1/databases/8/", 
                "tables": [
                    143, 
                    138, 
                    134, 
                    141, 
                    140, 
                    128, 
                    129, 
                    125, 
                    136, 
                    126, 
                    132, 
                    131, 
                    127, 
                    137, 
                    124, 
                    133, 
                    130, 
                    139, 
                    142, 
                    135
                ], 
                "id": 8, 
                "name": "tableizer", 
                "server": 1, 
                "cached_size": 6651904, 
                "created_at": "2013-05-03T13:53:45", 
                "updated_at": "2013-05-13T18:00:09"
            }, 
        ]
        
4. Get specific database

        curl http://localhost:8000/api/v1/databases/2/
        
        {
            "tables": [
                {
                    "url": "http://localhost:8000/api/v1/tables/47/", 
                    "server": 1, 
                    "id": 47, 
                    "name": "salaries", 
                    "schema": 2, 
                    "cached_size": 136511488, 
                    "created_at": "2013-05-03T13:53:44", 
                    "updated_at": "2013-05-13T18:00:07"
                }, 
                {
                    "url": "http://localhost:8000/api/v1/tables/48/", 
                    "server": 1, 
                    "id": 48, 
                    "name": "titles", 
                    "schema": 2, 
                    "cached_size": 31571968, 
                    "created_at": "2013-05-03T13:53:44", 
                    "updated_at": "2013-05-13T18:00:07"
                }, 
            ],
            "id": 2, 
            "name": "employees", 
            "server": 1, 
            "cached_size": 205979648, 
            "created_at": "2013-05-03T13:53:44", 
            "updated_at": "2013-05-13T18:00:09"
        }

5. Get all tables

        curl  http://localhost:8000/api/v1/tables/
        
        [
            {
                "url": "http://localhost:8000/api/v1/tables/47/", 
                "server": 1, 
                "id": 47, 
                "name": "salaries", 
                "schema": 2, 
                "cached_size": 136511488, 
                "created_at": "2013-05-03T13:53:44", 
                "updated_at": "2013-05-13T18:00:07"
            }, 
            {
                "url": "http://localhost:8000/api/v1/tables/48/", 
                "server": 1, 
                "id": 48, 
                "name": "titles", 
                "schema": 2, 
                "cached_size": 31571968, 
                "created_at": "2013-05-03T13:53:44", 
                "updated_at": "2013-05-13T18:00:07"
            }, 
        ]

6. Get specific table

        curl http://localhost:8000/api/v1/tables/47/
        
        {
            "id": 47, 
            "name": "salaries", 
            "schema": 2, 
            "cached_size": 136511488, 
            "created_at": "2013-05-03T13:53:44", 
            "updated_at": "2013-05-13T18:00:07"
        }

7. Tableizer History. Usage is similar to tableizer-query command.

        curl http://localhost:8000/api/v1/history/?since=11d
        
        {
            "definitions": {
                "2013-05-04 00:00:02": [
                    {
                        "diff": "--- auth_user_user_permissions\t2013-05-03 13:53:46\n+++ auth_user_user_permissions\t2013-05-04 00:00:09\n+++\nUNIQUE KEY `user_id` (`user_id`,`permission_id`),\nKEY `auth_user_user_permissions_6340c63c` (`user_id`),\nKEY `auth_user_user_permissions_83d7f98b` (`permission_id`),\n-  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),\n-  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)\n+  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),\n+  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)\n) ENGINE=InnoDB DEFAULT CHARSET=latin1", 
                        "status": "changed", 
                        "id": 116, 
                        "server": "localhost", 
                        "database_name": "tableizer", 
                        "table_name": "auth_user_user_permissions", 
                        "create_syntax": "CREATE TABLE `auth_user_user_permissions` (\n  `id` int(11) NOT NULL AUTO_INCREMENT,\n  `user_id` int(11) NOT NULL,\n  `permission_id` int(11) NOT NULL,\n  PRIMARY KEY (`id`),\n  UNIQUE KEY `user_id` (`user_id`,`permission_id`),\n  KEY `auth_user_user_permissions_6340c63c` (`user_id`),\n  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),\n  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),\n  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)\n) ENGINE=InnoDB DEFAULT CHARSET=latin1", 
                        "run_time": "2013-05-04T00:00:02", 
                        "created_at": "2013-05-04T00:00:09", 
                        "updated_at": "2013-05-04T00:00:09"
                    }, 
                    {
                        "diff": "--- auth_user_groups\t2013-05-03 13:53:46\n+++ auth_user_groups\t2013-05-04 00:00:09\n+++\nUNIQUE KEY `user_id` (`user_id`,`group_id`),\nKEY `auth_user_groups_6340c63c` (`user_id`),\nKEY `auth_user_groups_5f412f9a` (`group_id`),\n-  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),\n-  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)\n+  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),\n+  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)\n) ENGINE=InnoDB DEFAULT CHARSET=latin1", 
                        "status": "changed", 
                        "id": 115, 
                        "server": "localhost", 
                        "database_name": "tableizer", 
                        "table_name": "auth_user_groups", 
                        "create_syntax": "CREATE TABLE `auth_user_groups` (\n  `id` int(11) NOT NULL AUTO_INCREMENT,\n  `user_id` int(11) NOT NULL,\n  `group_id` int(11) NOT NULL,\n  PRIMARY KEY (`id`),\n  UNIQUE KEY `user_id` (`user_id`,`group_id`),\n  KEY `auth_user_groups_6340c63c` (`user_id`),\n  KEY `auth_user_groups_5f412f9a` (`group_id`),\n  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),\n  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)\n) ENGINE=InnoDB DEFAULT CHARSET=latin1", 
                        "run_time": "2013-05-04T00:00:02", 
                        "created_at": "2013-05-04T00:00:09", 
                        "updated_at": "2013-05-04T00:00:09"
                    }
                ]
            }
        }

8. Top Databases

        curl http://localhost:8000/api/v1/databases/top/?percent=0.0000001&lim=5&days=1000
        
        {
            "type": "top_Pct", 
            "databases": [
                {
                    "database": "tableizer", 
                    "percent_growth": 68.0, 
                    "server": "localhost"
                }
            ]
        }

8. Top Tables

        curl http://localhost:8000/api/v1/tables/top/?&lim=2
        
        {
            "type": "top_N", 
            "databases": [
                {
                    "table": "salaries", 
                    "database": "employees", 
                    "cached_size": 136511488, 
                    "server": "localhost"
                }, 
                {
                    "table": "titles", 
                    "database": "employees", 
                    "cached_size": 31571968, 
                    "server": "localhost"
                }
            ]
        }
