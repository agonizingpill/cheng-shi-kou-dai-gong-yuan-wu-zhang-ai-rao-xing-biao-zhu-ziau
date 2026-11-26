        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "障碍权重对比试算",
  "module": "权重对比试算",
  "caption": "权重对比试算",
  "detail": "同一批入口留档标记、同一个放行门槛下，对照现行权重与候选权重的误放行入口数。现场判定与两套分都齐了才出结论，改判后两套数一起更新并留档。",
  "path": "/trials",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "profile",
      "label": "偏好卡"
    },
    {
      "name": "weights_b",
      "label": "候选权重"
    },
    {
      "name": "threshold",
      "label": "放行门槛"
    },
    {
      "name": "state",
      "label": "状态"
    },
    {
      "name": "false_pass_a",
      "label": "现行误放"
    },
    {
      "name": "false_pass_b",
      "label": "候选误放"
    },
    {
      "name": "verdict",
      "label": "最新结论"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "draft_trial",
      "label": "建立对比试算",
      "path": "/trials/draft-trial",
      "fields": [
        {
          "name": "code",
          "label": "试算单号",
          "kind": "text",
          "initial": "TR-02"
        },
        {
          "name": "profile",
          "label": "偏好卡号",
          "kind": "text",
          "initial": "PR-10"
        },
        {
          "name": "weights_b",
          "label": "候选权重",
          "kind": "json",
          "initial": {
            "石阶": 1,
            "碎石": 5
          }
        },
        {
          "name": "threshold",
          "label": "放行门槛",
          "kind": "float",
          "initial": 0.7
        }
      ],
      "help": "两套权重共用该公园现场见证入口的留档标记与同一放行门槛。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "score",
      "label": "计算两套分",
      "path": "/trials/score",
      "fields": [
        {
          "name": "trial",
          "label": "试算单号",
          "kind": "text",
          "initial": "TR-01"
        }
      ],
      "help": "异步逐入口打分，中断后再次提交即可续跑，已算出的分接着用。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "judge_entry",
      "label": "现场判定与改判",
      "path": "/trials/judge-entry",
      "fields": [
        {
          "name": "trial",
          "label": "试算单号",
          "kind": "text",
          "initial": "TR-01"
        },
        {
          "name": "entrance",
          "label": "入口",
          "kind": "text",
          "initial": "PK-E1"
        },
        {
          "name": "passable",
          "label": "走得过",
          "kind": "bool",
          "initial": false
        }
      ],
      "help": "首次判定作业员即可提交；改判须复核员，改判后两套误放行数一起更新。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "conclusion_log",
      "label": "查询结论留档",
      "path": "/trials/conclusion-log",
      "fields": [
        {
          "name": "trial",
          "label": "试算单号",
          "kind": "text",
          "initial": "TR-01"
        }
      ],
      "help": "列出历次结论，改判前的旧结论照样能查。",
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
        export const key = "trials";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
