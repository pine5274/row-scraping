# row-scraping

[日本ボート協会HP](https://www.jara.or.jp/race/)大会情報に記載されているレース結果をスクレイピングし、csvとして出力する。

// TODO 他と同じdf変換にする

というかクラスがいらないからリファクタリングする。

/14 [00:16<00:02,  1.31s/it]<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)
<ipython-input-1-7edfd2c4d655>:84: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)