CREATE TABLE IF NOT EXISTS price_kline (
                                            symbol varchar(10)
                                            , start_time timestamp
                                            , close_time timestamp
                                            , interval varchar(5)
                                            , low_price real
                                            , high_price real
                                            , close_price real
                                            );