from django.test import TestCase
import qbeapp.joins as jns
import networkx as nx

class JoinsTestCase(TestCase):   
     
    dummy_pk_dict = {'a': 'id', 'b': 'id', 'c': 'id', 'd': 'id', 'e': 'id',
                    'f': 'id', 'g': 'id', 'i': 'id', 'j': 'id', 'k': 'id',
                    'l': 'id'}

    def setUp(self):
        graph = nx.Graph()
        graph.add_edge('a', 'b', fk={'b': 'fkid'})
        graph.add_edge('a', 'c', fk={'c': 'fkid'})
        graph.add_edge('a', 'd', fk={'d': 'fkid'})
        graph.add_edge('b', 'e', fk={'e': 'fkid'})
        graph.add_edge('b', 'f', fk={'f': 'fkid'})
        graph.add_edge('c', 'f', fk={'f': 'fkid'})
        graph.add_edge('c', 'j', fk={'j': 'fkid'})
        graph.add_edge('d', 'g', fk={'g': 'fkid'})
        graph.add_edge('e', 'i', fk={'i': 'fkid'})
        graph.add_edge('f', 'i', fk={'i': 'fkid'})
        graph.add_edge('j', 'k', fk={'k': 'fkid'})
        graph.add_edge('g', 'k', fk={'k': 'fkid'})
        graph.add_edge('g', 'l', fk={'l': 'fkid'})
        jns.graph = graph
        jns.primary_key_dict = self.dummy_pk_dict

    def test_join_on(self):
        join_dict = {"a": "fkclm"}
        self.assertEqual(jns.join_on('a', join_dict), 'a.fkclm')

    def test_build_inner_join(self):
        self.assertEqual(jns.build_inner_join('a', 'b'), 'INNER JOIN b ON b.fkid = a.id')
        self.assertEqual(jns.build_inner_join('d', 'g'), 'INNER JOIN g ON g.fkid = d.id')
        with self.assertRaisesMessage(jns.errs.QBEError, "Invalid nodes."):
            jns.build_inner_join('a', 'k')

    def test_joins_from_successors(self):
        dummy_a_joins = ['INNER JOIN c ON c.fkid = a.id',
                       'INNER JOIN j ON j.fkid = c.id', 
                       'INNER JOIN k ON k.fkid = j.id',
                       'INNER JOIN g ON k.fkid = g.id',
                       'INNER JOIN d ON g.fkid = d.id',
                       'INNER JOIN l ON l.fkid = g.id',
                       'INNER JOIN f ON f.fkid = c.id',
                       'INNER JOIN i ON i.fkid = f.id',
                       'INNER JOIN e ON i.fkid = e.id',
                       'INNER JOIN b ON e.fkid = b.id']
        self.assertItemsEqual(jns.joins_from_successors(jns.graph, 'a'), dummy_a_joins)
        self.assertListEqual(jns.joins_from_successors(jns.graph, 'a'), dummy_a_joins)
        dummy_d_joins = ['INNER JOIN a ON d.fkid = a.id',
                         'INNER JOIN c ON c.fkid = a.id', 
                         'INNER JOIN j ON j.fkid = c.id',
                         'INNER JOIN k ON k.fkid = j.id',
                         'INNER JOIN g ON k.fkid = g.id',
                         'INNER JOIN l ON l.fkid = g.id',
                         'INNER JOIN f ON f.fkid = c.id',
                         'INNER JOIN i ON i.fkid = f.id',
                         'INNER JOIN e ON i.fkid = e.id',
                         'INNER JOIN b ON e.fkid = b.id']
        self.assertItemsEqual(jns.joins_from_successors(jns.graph, 'd'), dummy_d_joins)
        self.assertListEqual(jns.joins_from_successors(jns.graph, 'd'), dummy_d_joins)