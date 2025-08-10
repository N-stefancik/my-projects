import random
import numpy as np
import copy
from collections import deque
from collections import defaultdict
import itertools

class DAG:
  def __init__(self):
    self.nodes = {}
    self.edges = []
    self.topological_order = []

  def add_node(self, name, states):
    node = Node(name, states)
    self.nodes[name] = node
    self.topological_order = self.sort_topologically()
    return node

  def add_edge(self, parent_name, child_name):
    parent = self.nodes[parent_name]
    child = self.nodes[child_name]
    child.add_parent_child(parent)
    self.edges.append((parent, child))




  def sort_topologically(self):
    #https://llego.dev/posts/implementing-topological-sort-python/

    nodes = self.nodes
    edges = self.edges
    indegree = defaultdict(int)
    queue = deque()
    topological_order = []


    for node_name in nodes:
      node = nodes[node_name]
      for child in node.children:
        indegree[child.name] += 1

    for node_name in nodes:
      if indegree[node_name] == 0:
        queue.append(nodes[node_name])

    while queue:
      node = queue.popleft()
      topological_order.append(node.name)

      for child in node.children:
        indegree[child.name] -= 1
        if indegree[child.name] == 0:
          queue.append(child)

    if len(topological_order) != len(nodes):
      print("Cycle exists")
    else:
      return topological_order



  def rejection_sampling(self, query_var, evidence_vars = None, num_samples = 2000):
        samples = []
        for _ in range(num_samples):
          sample = self.sample_from_prior()
          if self.matches_evidence(sample, evidence_vars):
            samples.append(sample)
          num = 0
          for sample in samples:
            query_key = next(iter(query_var))
            if query_var[query_key] == sample[query_key]:
               num+=1
        return num, len(samples), num_samples


  def sample_from_prior(self):
      #samples from the prior distribution doesn't use evidence vars
      sample = {}
      nodes = self.nodes
      for node_name in self.topological_order:
          parents = nodes[node_name].parents
          if len(parents) == 0:
              probs = list(nodes[node_name].table.get((), {}).values())
              sample[node_name] = np.random.choice(nodes[node_name].states, 1, p=probs)
          else:
              parent_values = tuple(sample[parent.name][0] for parent in parents)
              probs = list(nodes[node_name].table.get((parent_values), {}).values())
              sample[node_name] = np.random.choice(nodes[node_name].states, 1, p=probs)
      return sample


  def matches_evidence(self, sample, evidence_vars=None):
    if evidence_vars is None:
      return True
    for var in evidence_vars:
      if evidence_vars[var] != sample[var]:
        return False
    return True



  def gibbs_sampling(self, query_var, evidence_vars = None, num_samples = 4000):
    count = 0
    sample = self.sample_from_evidence(evidence_vars)
    query_key = next(iter(query_var))
    if sample[query_key] == query_var[query_key]:
      count += 1
    if evidence_vars is None:
      evidence_vars = {}
    evidence_keys = list(evidence_vars.keys())
    for _ in range(num_samples):
      sampling_node = self.random_node(evidence_vars)

      if sampling_node not in evidence_keys:
        new_evidence_vars = copy.deepcopy(sample)
        del new_evidence_vars[sampling_node]
      else:
        new_evidence_vars = copy.deepcopy(sample)
      sample = self.sample_from_evidence(new_evidence_vars)
      if sample[query_key] == query_var[query_key]:
        count += 1
    return count, num_samples

  def random_node(self, evidence_vars):
    nodes = self.nodes
    non_evidence_vars = [node_name for node_name in nodes if node_name not in evidence_vars]
    return np.random.choice(non_evidence_vars)

  def sample_from_evidence(self, evidence_vars):
    sample = {}
    nodes = self.nodes
    if evidence_vars is None:
      evidence_vars = {}
    for var in evidence_vars:
      sample[var] = evidence_vars[var]
    for node_name in self.topological_order:
      if node_name not in sample:
        parents = self.nodes[node_name].parents
        if len(parents) == 0:
          probs = list(self.nodes[node_name].table.get((), {}).values())
          sample[node_name] = np.random.choice(self.nodes[node_name].states, 1, p=probs)
        else:
          parent_values = tuple(sample[parent.name][0] for parent in parents)
          probs = list(nodes[node_name].table.get((parent_values), {}).values())
          sample[node_name] = np.random.choice(nodes[node_name].states, 1, p=probs)
    return sample

  def enumeration_ask(self, query_var, evidence_vars=None):
    if evidence_vars is None:
        evidence_vars = {}
    query_key = next(iter(query_var))
    query_value = query_var[query_key]
    prob_dist = {}

    for val in self.nodes[query_key].states:
        extended_evidence = evidence_vars.copy()
        extended_evidence[query_key] = np.array([val])
        prob_dist[val] = self.enumerate_all(self.topological_order, extended_evidence)

    normalized_distribution = self.normalize(prob_dist)

    return normalized_distribution[query_value]

  def enumerate_all(self, variables, evidence):
    if not variables:
        return 1.0

    Y = variables[0]
    rest_vars = variables[1:]

    if Y in evidence:
        y_value = evidence[Y][0]
        prob = self.get_conditional_probability(Y, y_value, evidence)
        return prob * self.enumerate_all(rest_vars, evidence)
    else:
        total = 0.0
        for y_value in self.nodes[Y].states:
            extended_evidence = evidence.copy()
            extended_evidence[Y] = np.array([y_value])
            prob = self.get_conditional_probability(Y, y_value, extended_evidence)
            total += prob * self.enumerate_all(rest_vars, extended_evidence)
        return total
  '''
  def get_conditional_probability(self, node_name, node_value, evidence):
      node = self.nodes[node_name]
      if len(node.parents) == 0:
          return node.table.get((), {}).get(node_value)
      parent_values = tuple(evidence[parent.name][0] for parent in node.parents)
      return node.table.get(parent_values, {}).get(node_value)
  '''
  def get_conditional_probability(self, node_name, node_value, evidence):
    node = self.nodes[node_name]
    if len(node.parents) == 0:
        # If no parents, use the prior probability
        prob = node.table.get((), {}).get(node_value)  
        # If prior probability is not found, return a default value (e.g., 0.5)
        return prob if prob is not None else 0.5  
    parent_values = tuple(evidence[parent.name][0] for parent in node.parents)
    # If conditional probability is not found, return a default value (e.g., 0.5)
    prob = node.table.get(parent_values, {}).get(node_value)  
    return prob if prob is not None else 0.5

  def normalize(self, distribution):
      total = sum(distribution.values())
      if total == 0:
          return {key: 0 for key in distribution}
      return {key: value / total for key, value in distribution.items()}

class Node:
    def __init__(self, name, states):
        self.name = name
        self.states = states
        self.parents = []
        self.children = []
        self.table = None

    def add_parent_child(self, parent):
      if parent not in self.parents:
          self.parents.append(parent)
          parent.children.append(self)

    def set_table(self, table):
        self.table = table
def parse_network_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]

    num_vars = int(lines[0])
    variables = []
    i = 1
    graph = DAG()

    for _ in range(num_vars):
        tokens = lines[i].split()
        var_name = tokens[0]
        domain = tokens[1:]
        graph.add_node(var_name, domain)
        variables.append(var_name)
        i += 1

    num_cpts = int(lines[i])
    i += 1
    for _ in range(num_cpts):
        cpt_lines = []
        while i < len(lines) and lines[i]:
            cpt_lines.append(lines[i])
            i += 1
        i += 1  # skip blank line

        header = cpt_lines[0].split('|')
        child = header[0].strip()
        parents = header[1].split() if len(header) > 1 else []
        for parent in parents:
            graph.add_edge(parent, child)

        states = graph.nodes[child].states
        parent_states = [graph.nodes[p].states for p in parents]
        entries = cpt_lines[1:]

        cpt_table = {}
        for idx, line in enumerate(entries):
            probs = list(map(float, line.strip().split()))
            outcome_probs = dict(zip(states, probs))
            if parents:
                parent_val_combo = tuple(prod[idx] for prod in zip(*parent_states))
                parent_vals = tuple(itertools.product(*parent_states))[idx]
                cpt_table[parent_vals] = outcome_probs
            else:
                cpt_table[('1',)] = outcome_probs
        graph.nodes[child].set_table(cpt_table)

    return graph

def parse_query_args(tokens):
    query_var = tokens[0]
    evidence = {}
    if len(tokens) > 2:
        evidence_tokens = tokens[2:]
        for pair in evidence_tokens:
            var, val = pair.split('=')
            evidence[var] = val
    return query_var, evidence

def repl():
    graph = None
    while True:
        try:
            cmd = input().strip()
        except EOFError:
            break  # graceful exit for autograder

        if cmd.startswith("load"):
            _, filename = cmd.split()
            graph = DAG()
            with open(filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]

            idx = 0
            num_vars = int(lines[idx])
            idx += 1

            # Load variables
            for _ in range(num_vars):
                parts = lines[idx].split()
                name, domain = parts[0], parts[1:]
                graph.add_node(name, domain)
                idx += 1

            num_cpts = int(lines[idx])
            idx += 1

            for _ in range(num_cpts):
                header = lines[idx].split()
                idx += 1
                var = header[0]
                parents = header[1:]
                for p in parents:
                    graph.add_edge(p, var)

                num_rows = 1
                if parents:
                    for p in parents:
                        num_rows *= len(graph.nodes[p].states)

                table = {}
                parent_domains = [graph.nodes[p].states for p in parents]
                parent_keys = list(itertools.product(*parent_domains)) if parents else [()]

                for key in parent_keys:
                    probs = list(map(float, lines[idx].split()))
                    idx += 1
                    state_probs = dict(zip(graph.nodes[var].states, probs))
                    table[key] = state_probs

                graph.nodes[var].set_table(table)

        elif cmd.startswith("xquery"):
            if graph is None:
                continue
            tokens = cmd.split()
            query_var, evidence = parse_query_args(tokens[1:])
            dist = {}
            for val in graph.nodes[query_var].states:
                dist[val] = graph.enumeration_ask({query_var: val}, evidence)
            print(" ".join(f"{dist[val]:.4f}" for val in graph.nodes[query_var].states))

        elif cmd.startswith("rquery"):
            if graph is None:
                continue
            tokens = cmd.split()
            query_var, evidence = parse_query_args(tokens[1:])
            counts = {}
            total = 0
            for val in graph.nodes[query_var].states:
                num, accepted, _ = graph.rejection_sampling({query_var: val}, evidence)
                counts[val] = num
                total += num
            dist = {k: v / total if total else 0 for k, v in counts.items()}
            print(" ".join(f"{dist[val]:.4f}" for val in graph.nodes[query_var].states))

        elif cmd.startswith("gquery"):
            if graph is None:
                continue
            tokens = cmd.split()
            query_var, evidence = parse_query_args(tokens[1:])
            counts = {}
            total = 0
            for val in graph.nodes[query_var].states:
                num, _ = graph.gibbs_sampling({query_var: val}, evidence)
                counts[val] = num
                total += num
            dist = {k: v / total if total else 0 for k, v in counts.items()}
            print(" ".join(f"{dist[val]:.4f}" for val in graph.nodes[query_var].states))

        elif cmd == "quit":
            break
if __name__ == "__main__":
    repl()
