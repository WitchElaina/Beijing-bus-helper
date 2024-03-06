import { useEffect, useState } from 'react';
import {
  Input,
  Button,
  Flex,
  Select,
  Result,
  Spin,
  Space,
  Typography,
  Card,
  Timeline,
} from 'antd';
import useSWR from 'swr';
import axios from 'axios';
import {
  SwapRightOutlined,
  SwapOutlined,
  SearchOutlined,
} from '@ant-design/icons';

const { Text, Link, Title } = Typography;

// API server
const API_SERVER = 'http://localhost:5002';

// use axios as fetcher
const fetcher = (url: string) =>
  axios.get(API_SERVER + url).then((res) => res.data);

function App() {
  const { data, error, isLoading } = useSWR('/station/list', fetcher);
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState([]);

  const switchStartEnd = () => {
    const temp = start;
    setStart(end);
    setEnd(temp);
  };

  const processPath = (
    allPath: {
      path: string;
      counts: number;
      stations: number;
    },
    curIndex: number,
  ) => {
    const lines = allPath.path
      .split('\n')
      .map((item) => item.trim())
      .filter((item) => item !== '');

    const lineStation = [];
    for (let i = 0; i + 1 < lines.length; i += 2) {
      lineStation.push({
        line: lines[i].substring(0, lines[i].indexOf(':')),
        station: lines[i + 1].split('->'),
      });
    }

    console.log(lineStation);

    const timelineChildren = [];
    lineStation.forEach((item, index, arr) => {
      const stations =
        arr.length > 1 && index !== arr.length - 1
          ? item.station.slice(0, arr.length)
          : item.station;

      stations.forEach((station, index) => {
        timelineChildren.push({
          key: station + item.line,
          children: station,
          label: index === 0 ? item.line : undefined,
        });
      });
    });

    return (
      <Card style={{ width: '400px' }} title={`方案${curIndex}`}>
        <Flex vertical gap={20} align="left">
          {/* <Title level={5} style={{ marginTop: 0 }}>
            共换乘{allPath.counts}次，经过{allPath.stations}站
          </Title> */}
          {
            <Timeline
              // items={item.station.map((station) => {
              //   return {
              //     key: station + item.line,
              //     children: station,
              //   };
              // })}
              mode="left"
              items={timelineChildren}
            ></Timeline>
          }
        </Flex>
      </Card>
    );
  };

  const search = () => {
    setLoading(true);
    axios.post(API_SERVER + '/search', { start, end }).then((res) => {
      setLoading(false);
      setResult(res.data.all_path);
    });
  };

  if (isLoading) {
    return <Spin fullscreen />;
  }

  if (error) {
    return <Result status="error" title="Error" subTitle={error.message} />;
  }
  console.log(data);

  return (
    <Flex vertical align="center" gap={20}>
      <Flex vertical align="center" gap={0}>
        <Title level={3} style={{ marginBottom: '2px' }}>
          北京公交换乘查询
        </Title>
        <Text type="secondary">
          Made by <Link>WitchElaina</Link>
        </Text>
        <Text type="secondary">
          Powered by <Link>Beijing-Bus-Helper</Link>
        </Text>
      </Flex>

      <Flex gap={5} align="center" style={{ marginTop: '20px' }}>
        <Text>从</Text>
        <Select
          placeholder="请选择起点"
          showSearch
          style={{ width: 200 }}
          options={data.stations.map((item: any) => ({
            label: item,
            value: item,
          }))}
          onChange={(value) => setStart(value)}
          value={start}
        ></Select>
        <Text>到</Text>
        <Select
          placeholder="请选择终点"
          showSearch
          style={{ width: 200 }}
          options={data.stations.map((item: any) => ({
            label: item,
            value: item,
          }))}
          onChange={(value) => setEnd(value)}
          value={end}
        ></Select>
        <Button onClick={switchStartEnd} icon={<SwapOutlined />} />
        <Button type="primary" icon={<SearchOutlined />} onClick={search}>
          查询
        </Button>
      </Flex>
      <Spin tip="正在搜索" spinning={loading}>
        <Flex gap={20} style={{ marginTop: '20px' }}>
          {result.length > 0 ? (
            result.map((item: any, index) => {
              return processPath(item, index + 1);
            })
          ) : (
            <Card>
              <Text type="secondary">请先输入起点和终点，然后点击查询按钮</Text>
            </Card>
          )}
        </Flex>
      </Spin>
    </Flex>
  );
}

export default App;
