        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "无障碍障碍组合",
  "module": "绕行偏好卡",
  "caption": "绕行偏好卡",
  "detail": "声明应避开的设施标记与优先级。多标签二值编码允许同一入口同时具有临时标线和碎石等特征。",
  "path": "/walk_profiles",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "park",
      "label": "公园"
    },
    {
      "name": "avoid",
      "label": "需避开标记"
    },
    {
      "name": "weights",
      "label": "标记权重"
    },
    {
      "name": "minimum",
      "label": "最低匹配分"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "draft_profile",
      "label": "记录绕行条件",
      "path": "/walk_profiles/draft-profile",
      "fields": [
        {
          "name": "code",
          "label": "偏好卡号",
          "kind": "text",
          "initial": "PR-11"
        },
        {
          "name": "park",
          "label": "公园",
          "kind": "text",
          "initial": "柳瓦园"
        },
        {
          "name": "avoid",
          "label": "应规避标记",
          "kind": "json",
          "initial": [
            "石阶",
            "碎石"
          ]
        },
        {
          "name": "weights",
          "label": "阻碍权重",
          "kind": "json",
          "initial": {
            "石阶": 2,
            "碎石": 1
          }
        },
        {
          "name": "minimum",
          "label": "最低匹配分",
          "kind": "float",
          "initial": 0.7
        }
      ],
      "help": "避开标记与权重键一一对应。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "match_entrances",
      "label": "计算地图候选入口",
      "path": "/walk_profiles/match-entrances",
      "fields": [
        {
          "name": "profile",
          "label": "偏好卡号",
          "kind": "text",
          "initial": "PR-11"
        }
      ],
      "help": "按障碍权重从高到低列出候选入口。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "false_passes",
      "label": "查询两套权重误放行入口",
      "path": "/trials/false-passes",
      "fields": [
        {
          "name": "trial",
          "label": "试算单号",
          "kind": "text",
          "initial": "TR-01"
        }
      ],
      "help": "对照现行与候选权重各自错放了哪些走不过的入口。",
      "roles": [
        "operator",
        "reviewer",
        "viewer"
      ],
      "success": "查询完成"
    }
  ]
};

        export const {title} = page;
        export const key = "walk_profiles";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
