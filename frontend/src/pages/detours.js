        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "步测绕行线路",
  "module": "绕行线路单",
  "caption": "绕行线路单",
  "detail": "维护员步测路段长度，使用编码结果提交入口。坡道不可通行或冲突标记过多时，现场改线。",
  "path": "/detours",
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
      "name": "entrance",
      "label": "终点入口"
    },
    {
      "name": "walk_m",
      "label": "绕行距离 m"
    },
    {
      "name": "score",
      "label": "匹配分"
    },
    {
      "name": "state",
      "label": "状态"
    }
  ],
  "layout": "flip",
  "view": "stack",
  "actions": [
    {
      "name": "submit_detour",
      "label": "提报步测线路",
      "path": "/detours/submit-detour",
      "fields": [
        {
          "name": "code",
          "label": "提报编号",
          "kind": "text",
          "initial": "DP-11"
        },
        {
          "name": "token",
          "label": "匹配任务",
          "kind": "token",
          "initial": ""
        },
        {
          "name": "entrance",
          "label": "绕行终点",
          "kind": "text",
          "initial": "PK-E2"
        },
        {
          "name": "walk_m",
          "label": "现场步测 m",
          "kind": "int",
          "initial": 76
        }
      ],
      "help": "选择计算过的终点，填入现场步测距离。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "withdraw_detour",
      "label": "退回已变化线路",
      "path": "/detours/withdraw-detour",
      "fields": [
        {
          "name": "detour",
          "label": "待退回线路单",
          "kind": "text",
          "initial": "DP-11"
        },
        {
          "name": "reason",
          "label": "现场变更简述",
          "kind": "text",
          "initial": "围挡向北移动"
        }
      ],
      "help": "仅待签注线路可退回重新步测。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "detours";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
